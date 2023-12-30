# -*- coding: UTF-8 -*-
import socket 
import threading
Local_Host = '127.0.0.1'
Local_Port = 10319
class ChatServer:
    db = {
    }   
    db_client = {

    }

    clients_list = []     #客户端列表

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    def create_listening_server(self):    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        local_ip = Local_Host
        local_port = Local_Port
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((local_ip, local_port))   
        print("Listening for incoming messages..")
        self.server_socket.listen(5) 
        self.receive_messages_in_a_new_thread()


    def receive_messages(self, so,client):
        return_msg = ""

        while True:
            try:
                incoming_buffer = so.recv(1024)
                if not incoming_buffer:
                    break
                login_msg = incoming_buffer.decode('utf-8')
                tag, info = login_msg.split('-',1)
                if tag == "1":                                             ## 登录
                    username,password = info.split('-')
                    if username in self.db and password==self.db.get(username):
                        return_msg = "1"
                    else :
                        return_msg = "0"
                    so.send(return_msg.encode('utf-8'))
                elif tag == "2": 
                    username,password = info.split('-')                    ## 注册
                    if username in self.db:
                        return_msg = "0"
                    else:
                        return_msg = "1"
                        self.db[username] = password
                    so.send(return_msg.encode('utf-8'))
                elif tag == "6":
                    message = "image from " + info
                    self.broadcast_to_all_clients(message)
                    image_data = so.recv((1<<20))
                    self.broadcast_to_all_clients(image_data,flag=False)
                elif tag == "4":
                    so.close()
                    break
            except:
                break
            if tag == "1" and return_msg == "1":
                msg =  username + " has joined"
                self.clients_list.append(client)
                self.db_client[username] = client
                self.broadcast_to_all_clients(msg) 
            elif tag == "3":
                username, msg = info.split('-',1)
                msg = username + ": " + msg
                self.broadcast_to_all_clients(msg)  
            elif tag == "5":
                username, info1 = info.split('-',1)
                touser,info = info1.split(':',1)
                touser = touser[1:]
                msg1 = "[private]from " + username + " " + info
                msg2 = "[private]to " + info1[1:]
                try:
                    self.broadcast_to_client(touser,msg1) 
                    self.broadcast_to_client(username,msg2) 
                except:
                    msg = "[private]该用户目前不在线"
                    self.broadcast_to_client(username,msg) 
        so.close()
        if client in self.clients_list:
            self.clients_list.remove(client)
            msg = username + " has left"
            self.broadcast_to_all_clients(msg)

    def broadcast_to_client(self, touser,msg,flag = True):
        socket, (ip, port) = self.db_client[touser]
        if(flag):
            socket.sendall(msg.encode('utf-8'))
        else :
            socket.sendall(msg)


    def broadcast_to_all_clients(self, msg,flag = True):
        for client in self.clients_list:
            socket, (ip, port) = client
            if(flag):
                socket.sendall(msg.encode('utf-8'))
            else :
                socket.sendall(msg)

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            print('There is a connection request from', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,client))
            t.start()



if __name__ == "__main__":
    ChatServer()