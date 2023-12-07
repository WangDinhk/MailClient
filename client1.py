from socket import *
import base64
import time

def get_email_address():
    email = input("Enter the email address: ")
    return email

msg = "\r\nI love you so much!"
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
receiver = get_email_address()  # Nhập địa chỉ email người nhận từ bàn phím

mailFrom = "MAIL FROM: " + sender + "\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
recv2 = recv2.decode()
print("After MAIL FROM command: " + recv2)
rcptTo = "RCPT TO: " + receiver + "\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
recv3 = recv3.decode()
print("After RCPT TO command: " + recv3)

data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()
print("After DATA command: " + recv4)

subject = "Subject: testing my client\r\n\r\n"
clientSocket.send(subject.encode())
date = time.strftime("%a, %d %b %Y %H:%M:%S ", time.gmtime())
date = date + "\r\n"
clientSocket.send(date.encode())
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:" + recv_msg.decode())

quit_command = "QUIT\r\n"
clientSocket.send(quit_command.encode())
recv5 = clientSocket.recv(1024)
print(recv5.decode())
clientSocket.close()
