import json
import socket
import os
import threading
from datetime import datetime

host = '0.0.0.0'
port = 8866
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
current_time = datetime.now()
client_sockets = []
print("正在加载文件")
if not os.path.exists('log'):
    os.makedirs('log')
    print('已在当前目录下创建 log 文件夹。')
if not os.path.exists('log.txt'):
    with open("log.txt", "w") as file:
        file.write("在 " + str(current_time) + " 创建此文件\n")
    print('已在当前目录下创建 log 文件夹。')
if not os.path.exists('Main.json'):
    data = {
        "Password": {
            "admin": "123456"
        }
    }
    with open('Main.json', 'w') as file:
        json.dump(data, file)
    print('已在当前目录下创建 Main.json 信息储存文件。')
print("文件加载完毕")


def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            print(f'客户端 {client_address} 断开连接')
            client_sockets.remove(client_socket)
            client_socket.close()
            break
        print(f'接收到来自客户端 {client_address} 的数据:', data)
        with open(os.path.join('log', f'{client_address}.txt'), 'a') as file:
            file.write(data + '\n')
        response = deal_message(data, client_address)
        client_socket.send(response.encode())


def deal_message(message, ip):
    msg_list = json.loads(message)
    if msg_list[0] == 'signin':
        if msg_list[1] <= 6 and msg_list[2] <= 10:
            response = sigh_in(message)
        else:
            response = "too_long"
    elif msg_list[0] == 'register':
        if msg_list[1] <= 6 and msg_list[2] <= 10:
            response = register(message)
        else:
            response = "too_long"
    else:
        response = None
    return response


def sigh_in(message):
    msg_list = json.loads(message)
    with open("Main.json", "r") as f:
        data = json.load(f).get("Password")
    username, user_password = msg_list[1], msg_list[2]
    for item in data:
        if item == username:
            if data[item] == user_password:
                response = "success"
            else:
                response = "wrong_password"
            break
    else:
        response = "wrong_name"
    return response


def register(message):
    msg_list = json.loads(message)
    new_username, new_password = msg_list[1], msg_list[2]
    with open("Main.json", "r") as f:
        data = json.load(f)
    if new_username in data["Password"]:
        response = "username_taken"
    else:
        data["Password"][new_username] = new_password
        with open("main.json", "w") as f:
            json.dump(data, f)
        response = "success"
    return response

print('服务器已开启，等待连接')
while True:
    client_socket, client_address = server_socket.accept()
    print(f'与客户端 {client_address} 连接成功')
    client_sockets.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
