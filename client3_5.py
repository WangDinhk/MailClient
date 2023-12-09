from socket import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_email_addresses():
    num_receivers = int(input("Enter the number of primary receivers: "))
    to_receivers = [input(f"Enter email address {i + 1} (TO): ") for i in range(num_receivers)]

    num_cc_receivers = int(input("Enter the number of CC receivers: "))
    cc_receivers = [input(f"Enter email address {i + 1} (CC): ") for i in range(num_cc_receivers)]

    num_bcc_receivers = int(input("Enter the number of BCC receivers: "))
    bcc_receivers = [input(f"Enter email address {i + 1} (BCC): ") for i in range(num_bcc_receivers)]

    return to_receivers, cc_receivers, bcc_receivers

def send_command(socket, command, expected_code):
    socket.send(command.encode())
    response = socket.recv(1024).decode()
    print(f"After {command.strip()} command: {response}")
    if response[:3] != expected_code:
        print(f'{expected_code} reply not received from the server.')
        socket.close()
        exit()

def send_email_to_single(to_address, sender):
    mailserver = ("127.0.0.1", 2225)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mailserver)

    send_command(clientSocket, '', '220')

    heloCommand = 'EHLO \r\n'
    send_command(clientSocket, heloCommand, '250')

    send_command(clientSocket, f"MAIL FROM: <{sender}>\r\n", '250')

    send_command(clientSocket, f"RCPT TO: <{to_address}>\r\n", '250')

    send_command(clientSocket, "DATA\r\n", '354')

    # Create a MIME message
    msg = MIMEMultipart()
    msg['Subject'] = "Testing my client"
    msg['From'] = sender
    msg['Bcc'] = to_address

    # Add the text part to the message
    text_part = MIMEText("I love computer networks!")
    msg.attach(text_part)

    # Add the MIME message to the socket
    clientSocket.send(msg.as_bytes())

    # Send the endmsg
    endmsg = "\r\n.\r\n"
    clientSocket.send(endmsg.encode())

    recv_msg = clientSocket.recv(1024).decode()
    print("Response after sending message body:" + recv_msg)

    send_command(clientSocket, "QUIT\r\n", '221')

    clientSocket.close()

def send_emails_to_bcc(bcc_receivers, sender):
    for bcc_recipient in bcc_receivers:
        send_email_to_single(bcc_recipient, sender)

def send_email(to_receivers, cc_receivers, sender):
    mailserver = ("127.0.0.1", 2225)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mailserver)

    send_command(clientSocket, '', '220')

    heloCommand = 'EHLO \r\n'
    send_command(clientSocket, heloCommand, '250')

    send_command(clientSocket, f"MAIL FROM: <{sender}>\r\n", '250')

    # Send RCPT TO command for each TO recipient
    for receiver in to_receivers:
        send_command(clientSocket, f"RCPT TO: <{receiver}>\r\n", '250')

    # Send RCPT TO command for each CC recipient
    for receiver in cc_receivers:
        send_command(clientSocket, f"RCPT TO: <{receiver}>\r\n", '250')

    send_command(clientSocket, "DATA\r\n", '354')

    # Create a MIME message
    msg = MIMEMultipart()
    msg['Subject'] = "Testing my client"
    msg['From'] = sender
    msg['To'] = ", ".join(to_receivers)
    msg['Cc'] = ", ".join(cc_receivers)

    # Add the text part to the message
    text_part = MIMEText("I love computer networks!")
    msg.attach(text_part)

    # Add the MIME message to the socket
    clientSocket.send(msg.as_bytes())

    # Send the endmsg
    endmsg = "\r\n.\r\n"
    clientSocket.send(endmsg.encode())

    recv_msg = clientSocket.recv(1024).decode()
    print("Response after sending message body:" + recv_msg)

    send_command(clientSocket, "QUIT\r\n", '221')

    clientSocket.close()

if __name__ == "__main__":
    to_receivers, cc_receivers, bcc_receivers = get_email_addresses()
    sender = "sender@fit.hcmus.edu.vn"

    send_email(to_receivers, cc_receivers, sender)
    
    if bcc_receivers:
        send_emails_to_bcc(bcc_receivers, sender)
