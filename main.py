#Do not change anything unless you know what your doing. It could brake the whole thing
import config.config
HOST = config.config.HOST
PORT = config.config.PORT
SERVER = config.config.SERVER





import libs.Date
import socket
import os
import threading
import libs.lemon
import sys
import libs.create_http
import pages.urls
import libs.HttpObject
import string
import random
import libs.handleHttp
sessions_  = {}




def init():
    global sock
    global HOST
    global PORT
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sock.bind((HOST, PORT))  
        sock.listen(socket.SOMAXCONN)
    except:
        sys.exit("Failed to start server")








    
def current_url():
    global PORT
    if PORT == 80:
        print("Server address: http://localhost/")
    else:
        print(f"Server address: http://localhost:{str(PORT)}/")











def get_random_string(length=config.config.token_length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def reset_session(data,id_):
    global sessions_
    if data[4].sessionReset:
        sessions_ = sessions_.pop(id_)
    else:
        sessions_[id_] = data[4].session

def handle_request(object):
    global sessions_
    if config.config.token in object.cookies:
        if object.cookies[config.config.token] in sessions_:
            id_ = object.cookies[config.config.token]
        else:
            id_ = get_random_string()
            object.new_cookies[config.config.token] = id_
            sessions_[id_] = {}
    else:
        id_ = get_random_string()
        object.new_cookies[config.config.token] = id_
        sessions_[id_] = {}
    object.session = sessions_[id_]
    
    data =  pages.urls.page(object)
    threading.Thread(target=reset_session,args=(data,id_)).start()
    return data





def handle_client(connection,address):
    if address[0] in config.config.blacklist:
        run = False
    else:
        run = True
    if run:


        headers=b""
        buffer_size = 4096
        while True:
            buf1 = connection.recv(buffer_size)
            headers += buf1
            if len(buf1) < buffer_size:
                break
            
            

        if headers.decode("utf-8","ignore").replace(" ","") != "":
            request_object = libs.handleHttp.http(headers,connection,address)
            print("Request: "+ request_object.page,end = "")
            print(" ",end="")
            object = libs.HttpObject.HttpObject(request_object.page,request_object.GET,request_object.POST,request_object.cookies,request_object.request_type)
            object.status ="200"
            object.FILES = request_object.FILES
            object.temp = request_object.temp
            object.headers = request_object.headers
            
            page_content = handle_request(object)
            DATA = libs.create_http.create(page_content)
            connection.send(DATA)
            connection.close()
            keys = list(page_content[4].FILES.keys())
            for x in range(len(keys)):
                try:
                    os.remove(f"{config.config.TEMP}/{page_content[4].FILES[keys[x]]['temp']}")
                except:
                    pass
        else:
            connection.close()
    else:
        connection.close()











def server_main():
    global sock
    while True:  
        try:
            connection,address = sock.accept()
            threading.Thread(target=handle_client, args=(connection,address)).start()
        except KeyboardInterrupt:
            sys.exit("\b\bShutting Down")























threading.Thread(target=current_url).start()
init()
server_main()