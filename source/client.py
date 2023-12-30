from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox 
import socket 
import threading 
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
import io

Local_Host = '127.0.0.1'
Local_Port = 10319

class Login(object):
    def __init__(self, root, client_socket):
        self.client_socket = client_socket
        self.reg = ''
        self.root = root
        self.varName = tkinter.StringVar(value='')
        self.varPwd = tkinter.StringVar(value='')
        self.root.resizable(0, 0)  
        self.totalName = tkinter.Label(self.root, text='LOGIN', justify=tkinter.RIGHT, width=180,font=("Helvetica", 20))
        self.labelName = tkinter.Label(self.root, text='用户名:', justify=tkinter.RIGHT, width=180)
        self.labelPwd = tkinter.Label(self.root, text='密码:', justify=tkinter.RIGHT, width=180)
        self.entryName = tkinter.Entry(self.root, width=180, textvariable=self.varName)
        self.entryPwd = tkinter.Entry(self.root, width=180, show='*', textvariable=self.varPwd)

        self.buttonOk = tkinter.Button(self.root, text='登录', command=self.login)
        self.buttonCancel = tkinter.Button(self.root, text='取消', command=self.cancel)
        self.buttonExchanage = tkinter.Button(self.root, text='注册', command=self.exchange)
        self.arrange()
    
    def arrange(self):                                
        self.totalName.place(x=250, y=30, width=100, height=50)
        self.labelName.place(x=100, y=100, width=100, height=80)
        self.labelPwd.place(x=100, y=180, width=100, height=80)
        self.entryName.place(x=250, y=130, width=200, height=30)
        self.entryPwd.place(x=250, y=210, width=200, height=30)
        self.buttonOk.place(x=100, y=300, width=80, height=40)
        self.buttonCancel.place(x=250, y=300, width=80, height=40)
        self.buttonExchanage.place(x=400, y=300, width=80, height=40)

    def login(self):
        name = self.entryName.get()
        pwd = self.entryPwd.get()
        if pwd == '' or name == '':
            tkinter.messagebox.showinfo(title='提示', message='请输入完整信息！')
        else:
            self.client_socket.send(("1-" + name + "-" + pwd).encode('utf-8'))
            buffer = self.client_socket.recv(1024)
            message = buffer.decode('utf-8')
            if message == "1":
                self.disappear()
                self.reg = CHAT(self.root, self.client_socket,name , pwd)
                tkinter.mainloop()
            else :
                self.cancel()
                tkinter.messagebox.showinfo(title='提示', message='用户名或密码输入错误，请重新尝试或注册新用户')


    def cancel(self):
        self.varName.set('')
        self.varPwd.set('')

    def disappear(self):   
        self.totalName.destroy()                            
        self.labelName.destroy()
        self.entryName.destroy()
        self.labelPwd.destroy()
        self.entryPwd.destroy()
        self.buttonOk.destroy()
        self.buttonCancel.destroy()
        self.buttonExchanage.destroy()

    def exchange(self):                           
        self.disappear()
        self.reg = Register(self.root,self.client_socket)
        self.reg.arrange()
        tkinter.mainloop()

    def on_close_window(self):
        if messagebox.askokcancel("退出", "确定退出吗?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)





class Register(object):
    def __init__(self, root,client_socket):
        self.client_socket = client_socket
        self.log = ''
        self.root = root
        self.varName = tkinter.StringVar(value='')
        self.varPwd1 = tkinter.StringVar(value='')
        self.varPwd2 = tkinter.StringVar(value='')
        self.totalName = tkinter.Label(self.root, text='REGISTER', justify=tkinter.RIGHT, width=350,font=("Helvetica", 20))
        self.labelName = tkinter.Label(self.root, text='用户名：', justify=tkinter.RIGHT, width=180)
        self.labelPwd1 = tkinter.Label(self.root, text='密码:', justify=tkinter.RIGHT, width=180)   
        self.labelPwd2 = tkinter.Label(self.root, text='重复密码：', justify=tkinter.RIGHT, width=180)
        self.entryName = tkinter.Entry(self.root, width=180, textvariable=self.varName)
        self.entryPwd1 = tkinter.Entry(self.root, width=180, show='*', textvariable=self.varPwd1)
        self.entryPwd2 = tkinter.Entry(self.root, width=180, show='*', textvariable=self.varPwd2)

        self.bottonsubmit = tkinter.Button(self.root, text='提交', command=self.register)
        self.bottonlogin = tkinter.Button(self.root, text='返回登录', command=self.exchange)
        self.arrange()

    def register(self):
        name = self.entryName.get()
        pwd1 = self.entryPwd1.get()
        pwd2 = self.entryPwd2.get()
        if name[0].isdigit():
            tkinter.messagebox.showinfo(title='提示', message='用户名不能以数字开头！')
            self.cancel()
        elif pwd2 == '' or pwd1 == '' or name == '':
            tkinter.messagebox.showinfo(title='提示', message='请输入完整信息！')
        elif pwd2 == pwd1:
            self.client_socket.send(("2-" + name + "-" + pwd1).encode('utf-8'))
            buffer = self.client_socket.recv(1024)
            message = buffer.decode('utf-8')
            if message == "1":
                self.disappear()
                tkinter.messagebox.showinfo(title='提示', message='注册成功！')
                self.reg = Login(self.root,self.client_socket)
                tkinter.mainloop()
            else :
                self.cancel()
                tkinter.messagebox.showinfo(title='提示', message='该用户名已被使用！')
        else:
            tkinter.messagebox.showinfo(title='提示', message='密码不一致，请重新输入。')
            self.cancel()
            
    def cancel(self):
        self.varName.set('')
        self.varPwd1.set('')
        self.varPwd2.set('')

    def arrange(self):

        self.totalName.place(x=250, y=30, width=150, height=50)
        self.labelName.place(x=100, y=100, width=100, height=80)
        self.labelPwd1.place(x=100, y=180, width=100, height=80)
        self.entryName.place(x=250, y=130, width=200, height=30)
        self.entryPwd1.place(x=250, y=210, width=200, height=30)

        self.labelPwd2.place(x=100, y=290, width=100, height=30)
        self.entryPwd2.place(x=250, y=290, width=200, height=30)

        self.bottonsubmit.place(x=180, y=350, width=80, height=40)
        self.bottonlogin.place(x= 330, y=350, width=80, height=40)

    def disappear(self):
        self.totalName.destroy()
        self.labelName.destroy()
        self.entryName.destroy()
        self.labelPwd1.destroy()
        self.entryPwd1.destroy()
        self.labelPwd2.destroy()
        self.entryPwd2.destroy()
        self.bottonsubmit.destroy()
        self.bottonlogin.destroy()

    def exchange(self):
        self.disappear()
        self.log = Login(self.root,self.client_socket)
        self.log.arrange()
        tkinter.mainloop()
    def on_close_window(self):
        if messagebox.askokcancel("退出", "确定退出吗?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)



class CHAT(object):
    def __init__(self, master,client_socket,name,pwd):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.password_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.client_socket = client_socket
        self.username = name
        self.thread = None
        self.pwd = pwd
        self.running_flag = True
        self.initialize_gui()                 
        self.listen_for_incoming_messages_in_a_thread()    


    def listen_for_incoming_messages_in_a_thread(self):
        self.thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))  
        self.thread.start()
    
    def receive_message_from_server(self, so):
        try:
            while self.running_flag:
                buffer = so.recv(1024) 
                if self.running_flag == False:
                    break
                if not buffer:
                    break
                message = buffer.decode('utf-8')
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
                if message.startswith("image from"):
                    image_data = so.recv((1<<20))
                    photo = ImageTk.PhotoImage(data = image_data)
                    self.chat_transcript_area.image_create('end', image=photo)
                    self.chat_transcript_area.insert('end', '\n')
        except:
            so.close()


    def initialize_gui(self): 
        self.frame1 = Frame()
        self.frame2 = Frame()
        self.frame3 = Frame()
        self.display_chat_box()
        self.display_chat_entry_box()
        self.bottonlogin = tkinter.Button(self.root, text='退出登录', command=self.exchange)
        self.bottonlogin.place(x= 330, y=430, width=80, height=40)

    def display_chat_box(self):
        Label(self.frame1, text='聊天区', font=("Serif", 12)).pack(side='top', anchor='w',pady=10)
        self.chat_transcript_area = Text(self.frame1, width=40, height=15, font=("Serif", 12),borderwidth=2)
        scrollbar = Scrollbar(self.frame1, command=self.chat_transcript_area.yview, orient=VERTICAL) 
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')  
        self.chat_transcript_area.pack(side='left', padx=0,pady=5)
        scrollbar.pack(side='left', fill='y')
        self.frame1.pack(side='top',anchor='n')

    def display_chat_entry_box(self):

        Label(self.frame2, text='请输入需要发送的消息:', font=("Serif", 12)).pack(side='left', anchor='w',pady=5)
        Button(self.frame2, text='发送图片', font=("Serif", 12),command=self.select_image).pack(side='left', anchor='w',pady=5)

        self.enter_text_widget = Text(self.frame3, width=40, height=2, font=("Serif", 12),borderwidth=2)
        self.hints =  Label(self.frame3,text='请输入:*[username]:+发送内容来进行私聊', font=("Serif", 12)).pack(side='top', anchor='w',pady=5)
        self.enter_text_widget.pack(side='top', padx=0,pady=5)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        self.frame2.pack(side='top',anchor='n')
        self.frame3.pack(side='top',anchor='n')

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])

        if file_path:
            message = ("6-" + self.username).encode('utf-8')
            self.client_socket.sendall(message)
            with Image.open(file_path) as img:
                img = img.resize((50, 50)) 

                with io.BytesIO() as output:
                    img.save(output, format='JPEG')  
                    image_data = output.getvalue()
            self.client_socket.sendall(image_data)


    def disappear(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.bottonlogin.destroy()

    def exchange(self):
        message = ("4-" + "l").encode('utf-8')
        self.client_socket.send(message)
        self.disappear()
        self.running_flag = False
        self.client_socket.close()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        remote_ip = Local_Host 
        remote_port = Local_Port 
        self.client_socket.connect((remote_ip, remote_port))
        self.log = Login(self.root,self.client_socket)

        self.log.arrange()
        tkinter.mainloop()

    def on_enter_key_pressed(self, event):
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        if data.startswith('*'):
            message = ("5-" + self.username  + "-" + data).encode('utf-8')
        else:
            message = ("3-" + self.username  + "-" + data).encode('utf-8')
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("退出", "确定退出吗?"):
            self.running_flag = False
            message = ("4-" + " ").encode('utf-8')
            self.client_socket.send(message)
            self.thread.join()
            self.root.destroy()
            self.client_socket.close()
            exit(0)


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    remote_ip = Local_Host 
    remote_port = Local_Port 
    client_socket.connect((remote_ip, remote_port)) 
    root = Tk()
    root.title('简易聊天室')
    root.geometry('600x500')
    root.resizable(1,1)
    gui = Login(root,client_socket)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()