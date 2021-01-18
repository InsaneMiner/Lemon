#cython: language_level=3

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
import libs.colors
import time
import re
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
    except OSError as exc:
        if exc.errno == 98:
            sys.exit(libs.colors.colors.fg.lightred+"Error: Another application is using this address/port"+libs.colors.colors.reset)
        sys.exit(libs.colors.colors.fg.lightred+"Error: Failed to start server for unknow reason. \nError code: "+str(exc)+libs.colors.colors.reset)
    except Exception as e:
        sys.exit(libs.colors.colors.fg.lightred+"Error: Failed to start server for unknow reason. \nError code: "+str(e)+libs.colors.colors.reset)
    
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
    start_time = time.time()
    if address[0] in config.config.blacklist:
        run = False
    else:
        run = True
    if run:
        buffer_size = 4096
        http_request = {"data": b"","body": b"","request_size": 0}
        current_http_status = 0
        _ = 0
        bad_request = 0
        while True:
            buf1 = connection.recv(buffer_size)
            http_request["data"] = http_request["data"] + buf1

            if "\r\n\r\n" in http_request["data"].decode("utf-8",errors="ignore") and current_http_status != 1:
                if  re.findall(r"Host:\s(.*)", http_request["data"].decode("utf-8",errors="ignore")) != []:
                    if re.findall(r"Content\-Length:\s([0-9]{1,})", http_request["data"].decode("utf-8",errors="ignore")) == []:
                        break
                    else:
                        http_request["body"] = bytes(http_request["data"].decode("utf-8",errors="ignore").split("\r\n\r\n")[1],"utf-8")
                else:
                    bad_request = 1
                    print("[!] Bad Request")
                    break
            elif current_http_status == 1:
                http_request["body"] = http_request["data"] + buf1

            if http_request["request_size"] == 0:
                try:
                    content_length = re.findall(r"Content\-Length:\s([0-9]{1,})", http_request["data"].decode("utf-8",errors="ignore"))
                    if content_length == []:
                        pass
                    else:
                        http_request["request_size"] = int(content_length[0])
                        
                except Exception as e:
                    print(e)
            elif len(http_request["body"]) >= http_request["request_size"]:
                break
            _ += 1 
        if bad_request == 1:
            try:
                connection.sendall(libs.create_http.create_error("Bad Request","400"))
                connection.close()
            except Exception as e:
                print(e)
        else:
            headers = http_request["data"]
            if headers.decode("utf-8",errors="ignore").replace(" ","") != "":
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
    time_took = time.time() - start_time
    if time_took > 3.0:
        time_message = f"{libs.colors.colors.fg.red}{time_took}{libs.colors.colors.reset}"
    else:
        time_message = f"{libs.colors.colors.fg.green}{time_took}{libs.colors.colors.reset}"
    time_message_print = f"It took {time_message} seconds to proccess and return request\n"
    sys.stdout.write(time_message_print)
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