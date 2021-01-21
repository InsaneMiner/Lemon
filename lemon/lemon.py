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
import asyncio
import libs.logging
import signal
sessions_  = {}





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

def log_info(object,time_took,address,request_full_url,dateandtime):
    with open(config.config.LOG_LOCATION,"a+") as log_file:
        log_file.write(f"TIMETOOK[{time_took}] DATE&TIME[\"{dateandtime}\"] IP[{address[0]}] URL[\"{object.url}\"] REQUEST[\"{request_full_url}\"] STATUS[{object.status}]\n")



async def handle_client(reader,writer):
    dateandtime = libs.Date.httpdate()
    address = writer.get_extra_info('peername')
    start_time = time.time()
    if address[0] in config.config.blacklist:
        run = False
    else:
        run = True
    if run:
        buffer_size = config.config.SOCKET_BUFFER

        http_request = {"data": b"","body": b"","request_size": 0}
        current_http_status = 0
        bad_request = 0
        while True:
            buf1 = await reader.read(buffer_size)
            http_request["data"] = http_request["data"] + buf1
            if "\r\n\r\n" in http_request["data"].decode("utf-8",errors="ignore") and current_http_status != 1:
                if  re.findall(r"Host:\s(.*)", http_request["data"].decode("utf-8",errors="ignore")) != []:
                    if re.findall(r"Content\-Length:\s([0-9]{1,})", http_request["data"].decode("utf-8",errors="ignore")) == []:
                        break
                    else:
                    
                        current_http_status = 1
                        http_request["body"] = bytes(http_request["data"].decode("utf-8",errors="ignore").split("\r\n\r\n")[1],"utf-8")
                else:
                    bad_request = 1
                    print("[!] Bad Request")
                    break
            elif current_http_status == 1:
               
                http_request["body"] = http_request["body"] + buf1

            if http_request["request_size"] == 0:
                try:
                    content_length = re.findall(r"Content\-Length:\s([0-9]{1,})", http_request["data"].decode("utf-8",errors="ignore"))
                    if content_length == []:
                        pass
                    else:
                        http_request["request_size"] = int(content_length[0])
                except Exception as e:
                    print(e)
            elif http_request["request_size"] <= sys.getsizeof(str(http_request["body"])):
                break
            print(http_request["request_size"], sys.getsizeof(str(http_request["body"])))

        

        if bad_request == 1:
            try:
                writer.write(libs.create_http.create_error("Bad Request","400"))
                await writer.drain()
                writer.close()
            except Exception as e:
                print(e)
        else:
            headers = http_request["data"]
            if headers.decode("utf-8",errors="ignore").replace(" ","") != "":
                request_full_url = headers.decode("utf-8",errors="ignore").split("\r\n")[0]
                request_object = libs.handleHttp.http(headers)
                if request_object.headers["Host"].split(":")[0] not in config.config.ALLOWED_HOSTS:
                    writer.write(libs.create_http.create_error("Bad Request, Host header incorrect","400"))
                    await writer.drain()
                    writer.close()
                else:                
                    print("Request: "+ request_object.page,end = "")
                    print(" ",end="")
                    object = libs.HttpObject.HttpObject(request_object.page,request_object.GET,request_object.POST,request_object.cookies,request_object.request_type)
                    object.status ="200"
                    object.FILES = request_object.FILES
                    object.temp = request_object.temp
                    object.headers = request_object.headers
                    page_content = handle_request(object)
                    DATA = libs.create_http.create(page_content)
                    writer.write(DATA)
                    await writer.drain()
                    writer.close()
                    keys = list(page_content[4].FILES.keys())
                    for x in range(len(keys)):
                        try:
                            os.remove(f"{config.config.TEMP}/{page_content[4].FILES[keys[x]]['temp']}")
                        except:
                            pass
            else:
                writer.close()
    else:
        writer.close()
    time_took = time.time() - start_time
    if time_took > 3.0:
        time_message = f"{libs.colors.colors.fg.red}{time_took}{libs.colors.colors.reset}"
    else:
        time_message = f"{libs.colors.colors.fg.green}{time_took}{libs.colors.colors.reset}"
   
    libs.logging.log("It took ")
    libs.logging.log(time_message)
    libs.logging.log(" seconds to proccess and return request\n")
    log_info(page_content[4],time_took,address,request_full_url,dateandtime)

    return 0

def server_main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_client, HOST,PORT, loop=loop)
    try:
        server = loop.run_until_complete(coro)
    except OSError as sock_error:
        if sock_error.errno == 98:
            libs.logging.error("Socket already in use. Exiting...")
            sys.exit(0)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        try:
            server.close()
            loop.close()
        except:
            pass
        libs.logging.good("\b\bShutting Down\n")
        sys.exit(0)
server_main()