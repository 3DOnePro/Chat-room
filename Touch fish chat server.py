# -*- coding: utf-8 -*-
# 聊天服务器
# 2021年7月4日

import socket
import os
import hashlib
from datetime import datetime
from threading import Thread
from playsound import playsound
from cryptography.fernet import Fernet #AES加解密
from colorama import Fore, init, Back

# 初始化colorama颜色
init(autoreset=True)

print("""
   ______ __            __     ______ _        __       _____                               
  / ____// /_   ____ _ / /_   / ____/(_)_____ / /_     / ___/ ___   _____ _   __ ___   _____
 / /    / __ \ / __ `// __/  / /_   / // ___// __ \    \__ \ / _ \ / ___/| | / // _ \ / ___/
/ /___ / / / // /_/ // /_   / __/  / /(__  )/ / / /   ___/ //  __// /    | |/ //  __// /    
\____//_/ /_/ \__,_/ \__/  /_/    /_//____//_/ /_/   /____/ \___//_/     |___/ \___//_/      
""")
print(Fore.LIGHTCYAN_EX+"▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  0.1Release版本  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ▱  ")

# 启动时间
date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print ("┌────────────────────────────┐")
print (f"│启动时间:{date_now}│")
print ("└────────────────────────────┘")

# 获取本机ip
myname = socket.getfqdn(socket.gethostname(  ))

# 获取本机电脑名
myaddr = socket.gethostbyname(myname)
print("计算机名称:",myname)
print("本机IP:",myaddr)

# 生成AES密钥
key = Fernet.generate_key()
f = Fernet(key)
string = key.decode("utf-8","replace")#bytes转化字符串
print ("加密密钥:",string)

# 设置加入邀请码
Invitation = input ("设置加入邀请码:") 

# 设置服务器端口
while True:
    try:
        port = int(input("设置服务器端口（0-65535）:"))
        break
    except ValueError:
        print("您输入的内容太奇怪，请再次尝试输入！！！")

# 服务器的IP地址
SERVER_HOST = "0.0.0.0"
SERVER_PORT = port  # 设置服务器端口
separator_token = " ：" # 我们将使用它来分隔客户端名称和消息

# 初始化所有连接的客户端套接字的列表/集
client_sockets = set()
# 创建一个TCP套接字
s = socket.socket()
# 将端口设为可用端口
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
# 将套接字绑定到我们指定的地址
s.listen(50)
print(f"监听端口: {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    监听来自客户端的发来的信息
    """
    while True:
        try:
            # 继续监听来自 `cs` 套接字的消息
            msg = cs.recv(1024).decode()
        except Exception as e:
            # 客户端不再连接
            # 从集合中删除
            print(f"{Back.RED}[{date_now}]错误:{e}")
            playsound("notification.mp3")
            client_sockets.remove(cs)
        # 迭代所有连接的套接字
        for client_socket in client_sockets:
            # 并发送消息
            client_socket.send(msg.encode()) 

while True:
    '''
    认证客户端是否合法
    '''
    # 一直接收新的用户
    client_socket, client_address = s.accept() 
    #随机字节发送给客户端
    rud = os.urandom(32)  #随机字节
    client_socket.send(rud)#发给客户端
    m_rud = client_socket.recv(32)
    miyao = Invitation+ string #加上key认证是不是和服务器一样
    shal = hashlib.md5(miyao.encode("utf-8"))#md5加密
    shal.update(rud)
    r_rud = shal.hexdigest().encode("utf-8")
    if r_rud == m_rud:
        client_socket.send(f"{Fore.LIGHTGREEN_EX}>>>服务端提示：连接服务器成功，开始愉快的聊天:D".encode("utf-8"))
        print (f"{Fore.LIGHTGREEN_EX}[{date_now}]用户{client_address} 加入成功！")
        # 将新连接的客户端添加到连接的套接字
        client_sockets.add(client_socket)
        # 启动一个新线程来侦听每个客户端的消息
        t = Thread(target=listen_for_client, args=(client_socket,))
        # 设置线程守护程序，使其在主线程结束时结束
        t.daemon = True
        # 启动线程
        t.start()
    else:
        print (f"{Fore.LIGHTYELLOW_EX}[{date_now}]已拒绝非法用户{client_address} 加入")
        client_socket.send(f"{Fore.LIGHTYELLOW_EX}>>>服务端提示：拒绝非法客户端加入服务器".encode("utf-8"))
        client_socket.close()


# 关闭客户端套接字
for cs in client_sockets:
    cs.close()
    # 关闭服务器套接字
    s.close()