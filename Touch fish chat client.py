# -*- coding: utf-8 -*-
# 聊天客户端
# 2021年7月4日

import socket
from socket import gethostbyname
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back, Style
from socket import gethostbyname
from lxml import etree
import requests
import datetime
from cryptography.fernet import Fernet 
import base64
import hashlib

# 初始化colorama颜色
init(autoreset=True)

print("""
  ╭──────────────────────────────────────────────────────────╮
　│    0.1Release版本                                         │
　│                                                           │
　│                                                 .--.      │
　│                                              .-(    ).    │
　│                                            (_•••26℃_)_)  │
　│───────────────────────────────────────────────────────────│
　│─═════════════════════════════════════════════════════════─│
　╰─═════════════════════════════════════════════════════════─╯
        _/¯      _/¯        _/¯        _/¯        _/¯   
      _/       _/         _/         _/         _/    
            Touch the fish chat room 24小时空气调节           
""")

# 获取本机电脑名
myname = socket.getfqdn(socket.gethostname(  ))

# 获取本机ip
myaddr = socket.gethostbyname(myname)
print("计算机名称:",myname)
print("本机IP:",myaddr)

while True:
    try:
        '''
        用户输入key
        '''
        # 把key处理一下
        aeskey = input("请输入密钥:").encode()
        akey = base64.b64encode(aeskey)
        bkey = base64.b64decode(akey)# 令人迷惑的操作¯\_(ツ)_/¯
        f = Fernet(bkey)
        string = bkey.decode("utf-8","replace")#bytes转化字符串
        break
    except Exception as e:
            print(f"{Back.RED}Key格式错误，请再次输入！！！")

# 加入邀请码
Invitation = input ("输入聊天摸鱼邀请码:")

# 初始化TCP套接字
s = socket.socket()

while True:
    try:
        '''
        设置服务器IP和端口
        '''
        # 输入服务器IP地址 
        serverip = input('请输入服务器地址:')
        # 输入服务器的端口        
        port = int(input('请输入服务器端口:'))
        SERVER_HOST = serverip# 服务器IP
        SERVER_PORT = port # 服务器的端口
        separator_token = ": " # 我们将使用它来分隔客户端名称和消息

        print(f"正在连接 {SERVER_HOST}:{SERVER_PORT}...")
        # 连接到服务器
        s.connect((SERVER_HOST, SERVER_PORT))
        # 接收并用md5进行加密处理,然后发送给服务端
        rud = s.recv(32)
        miyao = Invitation + string#加上key，验证服务器key是否相同
        shal = hashlib.md5(miyao.encode("utf-8"))
        shal.update(rud)
        m_rud = shal.hexdigest().encode("utf-8")
        s.send(m_rud)
        #接收认证信息
        r_msg = s.recv(100).decode("utf-8")# 这个函数真的太坑了
        print(r_msg)
        break
    except Exception as e:
        print(f"{Back.RED}[!]连接服务器失败:{e}")

# 展示所有的颜色
print ("───────────────────────────────────────────")
print (Fore.LIGHTRED_EX+"■",Fore.RED+"■",Fore.LIGHTMAGENTA_EX+"■",Fore.MAGENTA+"■",
       Fore.BLUE+"■",Fore.LIGHTBLUE_EX+"■",Fore.CYAN+"■",Fore.LIGHTCYAN_EX+"■",
       Fore.LIGHTGREEN_EX+"■",Fore.GREEN+"■",Fore.YELLOW+"■",Fore.LIGHTYELLOW_EX+"■",
       Fore.LIGHTWHITE_EX+"■",Fore.WHITE+"■",Fore.LIGHTBLACK_EX+"■")
print(Style.RESET_ALL,"1  2  3  4  5  6  7  8  9 10 11 12 13 14 15")

while True:
    try:
        '''
        个性化颜色
        '''
        color = int(input("选择聊天文字颜色(1-15):"))
        # 设置字符串颜色
        if color == 1:
            client_color = Fore.LIGHTRED_EX
            break
        elif color == 2:
            client_color = Fore.RED
            break
        elif color == 3:
            client_color = Fore.LIGHTMAGENTA_EX
            break
        elif color == 4:
            client_color = Fore.MAGENTA
            break
        elif color == 5:
            client_color = Fore.BLUE
            break
        elif color == 6:
            client_color = Fore.LIGHTBLUE_EX
            break
        elif color == 7:
            client_color = Fore.CYAN
            break
        elif color == 8:
            client_color = Fore.LIGHTCYAN_EX
            break
        elif color == 9:
            client_color = Fore.LIGHTGREEN_EX
            break
        elif color == 10:
            client_color = Fore.GREEN
            break
        elif color == 11:
            client_color = Fore.YELLOW
            break
        elif color == 12:
            client_color = Fore.LIGHTYELLOW_EX
            break
        elif color == 13:
            client_color = Fore.LIGHTWHITE_EX
            break
        elif color == 14:
            client_color = Fore.WHITE
            break
        elif color == 15:
            client_color = Fore.LIGHTBLACK_EX
        else:
            print (f"{Back.RED}输入1-15的数字！！！")
    except ValueError:
        print(f"{Back.RED}输入的内容必须是纯数字！！！")

# 提示客户输入名字
name = input("输入你的名字: ")

print ("输入聊天内容回车└→发送：")
def listen_for_messages():
    while True:
        message = s.recv(1024)
        sb = f.decrypt(message)# 解密字节串
        print ("\n"+sb.decode()+"\n输入聊天内容：")

# 创建一个线程来侦听此客户端的消息并打印它们
t = Thread(target=listen_for_messages)
# 设置线程守护程序，使其在主线程结束时结束
t.daemon = True
# 启动线程
t.start()

while True:
    # 我们要发送到服务器的输入消息
    src = input("")
    # 退出程序的方法
    if src.lower() == 'q':
        break
    # 添加日期时间，名称和发件人的颜色
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    src = f"{client_color}[{date_now}] {name}{separator_token}{src}{Fore.RESET}"
    # 生成加密字节串
    srcBytes = src.encode("utf-8")
    token = f.encrypt(srcBytes)
    # 最后，发送消息
    s.send(token)

# 结束
s.close()
