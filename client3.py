from socket import *
import base64
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_email_addresses(prompt, recipient_type):
    num_recipients = int(input(f"Enter the number of {recipient_type} recipients: "))
    recipients = []
    for i in range(num_recipients):
        email = input(f"Enter {recipient_type} email address {i + 1}: ")
        recipients.append(email)
    return recipients

def create_email(sender, recipients, cc_recipients=None, bcc_recipients=None):
    msg = MIMEMultipart()
    msg['From'] = sender

    if recipients:
        msg['To'] = ', '.join(recipients)

    if cc_recipients:
        msg['Cc'] = ', '.join(cc_recipients)
        recipients = recipients + cc_recipients if recipients else cc_recipients

    if bcc_recipients:
        recipients = recipients + bcc_recipients if recipients else bcc_recipients

    msg.attach(MIMEText("I love computer networks!", 'plain'))
    msg['Subject'] = "Testing my client"

    date = time.strftime("%a, %d %b %Y %H:%M:%S ", time.gmtime())
    date = date + "\r\n"
    msg.attach(MIMEText(date, 'plain'))

    return msg, recipients


msg = "\r\nI love computer networks!"
endmsg = "\r\n.\r\n"
mailserver = ("127.0.0.1", 2225)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
recv = recv.decode()
print("Message after connection request:" + recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

heloCommand = 'EHLO \r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
recv1 = recv1.decode()
print("Message after EHLO command:" + recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

sender = "sender@fit.hcmus.edu.vn"

# Prompt user to choose sending method
print("Choose sending method:")
print("1. TO")
print("2. CC")
print("3. BCC")

method_choice = input("Enter the number corresponding to the sending method: ")

receivers = cc_recipients = bcc_recipients = None

if method_choice == '1':
    receivers = get_email_addresses("Enter the number of TO", "TO")
elif method_choice == '2':
    cc_recipients = get_email_addresses("Enter the number of CC", "CC")
elif method_choice == '3':
    bcc_recipients = get_email_addresses("Enter the number of BCC", "BCC")
else:
    print("Invalid choice. Exiting.")
    clientSocket.close()
    exit()

mailFrom = "MAIL FROM: " + sender + "\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
recv2 = recv2.decode()
print("After MAIL FROM command: " + recv2)

if receivers:
    for receiver in receivers:
        rcptTo = "RCPT TO: " + receiver + "\r\n"
        clientSocket.send(rcptTo.encode())
        recv3 = clientSocket.recv(1024)
        recv3 = recv3.decode()
        print(f"After RCPT TO {receiver} command: " + recv3)

if cc_recipients:
    for cc_receiver in cc_recipients:
        rcptTo = "RCPT TO: " + cc_receiver + "\r\n"
        clientSocket.send(rcptTo.encode())
        recv_cc = clientSocket.recv(1024)
        recv_cc = recv_cc.decode()
        print(f"After RCPT TO (CC) {cc_receiver} command: " + recv_cc)

if bcc_recipients:
    for bcc_receiver in bcc_recipients:
        rcptTo = "RCPT TO: " + bcc_receiver + "\r\n"
        clientSocket.send(rcptTo.encode())
        recv_bcc = clientSocket.recv(1024)
        recv_bcc = recv_bcc.decode()
        print(f"After RCPT TO (BCC) {bcc_receiver} command: " + recv_bcc)

data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()
print("After DATA command: " + recv4)

email_msg, all_recipients = create_email(sender, receivers, cc_recipients, bcc_recipients)

clientSocket.send(email_msg.as_string().encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:" + recv_msg.decode())

quit_command = "QUIT\r\n"
clientSocket.send(quit_command.encode())
recv5 = clientSocket.recv(1024)
print(recv5.decode())
clientSocket.close()
