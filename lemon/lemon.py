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
import base64
import cProfile, pstats
import concurrent.futures



sessions_  = {}





def get_random_string(length=config.config.token_length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def reset_session(data,id_):
    global sessions_
    if data[1].sessionReset:
        sessions_ = sessions_.pop(id_)
    else:
        sessions_[id_] = data[1].session

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



# Content-Type header: Content\-Type\:\smultipart/form\-data\;\sboundary\=(.*?)\n$
# 


async def handle_client(reader,writer):
    prof = cProfile.Profile()
    timed_out = 0
    try:
        dateandtime = libs.Date.httpdate()
        address = writer.get_extra_info('peername')
        start_time = time.time()
        if address[0] in config.config.blacklist:
            run = False
        else:
            run = True
        if run:

            prof.enable()
            buffer_size = config.config.SOCKET_BUFFER
            http_request = {"data": b"","body": b"","request_size": 0}
            current_http_status = 0
            bad_request = 0
            command_type_varified = None
            content_length = None
            checked_for_type = 0
            multi_part_form_data_splitter = []
            length_of_splitter = 100
            while True:
                buf1 = await reader.read(buffer_size)
                http_request["data"] += buf1
                if  current_http_status != 1:
                    if "\r\n\r\n" in http_request["data"].decode("utf-8",errors="ignore"):
                        if  re.findall(r"Host:\s(.*)", http_request["data"].decode("utf-8",errors="ignore")) != []:
                            if re.findall(r"Content\-Length:\s([0-9]{1,})", http_request["data"].decode("utf-8",errors="ignore")) == []:
                                break
                            else:
                                current_http_status = 1
                                http_request["body"] = bytes(http_request["data"].decode("utf-8",errors="ignore").split("\r\n\r\n")[1],"utf-8")
                            
                                multi_part_form_data_splitter = re.findall(r"Content\-Type\: multipart/form\-data\; boundary\=(.*?)\r\n", http_request["data"].decode("utf-8",errors="ignore"))
                                multi_part_form_data_splitter_full = f"--{multi_part_form_data_splitter[0]}--"
                                if http_request["data"].decode("utf-8",errors="ignore")[:3].lower() == "get":
                                    break
                        else:
                            bad_request = 1
                            libs.logging.error("[!] Bad Request\n")
                            break
                if current_http_status == 1:
                    http_request["body"] += buf1 
                if command_type_varified != "POST" and checked_for_type != 1:
                    checked_for_type = 1
                    command_type = http_request["data"].decode("utf-8",errors="ignore")[:4]
                    if command_type.lower() == "post" and command_type_varified == None:
                        command_type_varified = "POST"
                if http_request["request_size"] == 0:
                    try:
                        content_length = re.findall(r"Content\-Length:\s([0-9]{1,})", http_request["data"].decode("utf-8",errors="ignore"))
                        if content_length == []:
                            pass
                        else:
                            http_request["request_size"] = int(content_length[0])
                    except Exception as e:
                        print(e)
                if command_type_varified == "POST" and multi_part_form_data_splitter != []:
                    '''
                    if multi_part_form_data_splitter == []:
                        multi_part_form_data_splitter = re.findall(r"Content\-Type\: multipart/form\-data\; boundary\=(.*?)\r\n", http_request["data"].decode("utf-8",errors="ignore"))
                        length_of_splitter = len(f"--{multi_part_form_data_splitter[0]}--")
                        multi_part_form_data_splitter_full = f"--{multi_part_form_data_splitter[0]}--"
                    '''
                    
                    if multi_part_form_data_splitter_full in http_request["body"][:length_of_splitter].decode("utf-8",errors="ignore"):
                        break
                if content_length != None:
                    if len(http_request["body"]) >= int(content_length[0]):
                        break
                if buf1 == "":
                    timed_out = 1 
                    break


            prof.disable()
            stats = pstats.Stats(prof).sort_stats('cumtime')
            stats.print_stats()
            if bad_request == 1:
                try:
                    writer.write(libs.create_http.create_error("Bad Request","400"))
                    await writer.drain()
                    writer.close()
                except Exception as e:
                    libs.logging.error(e)
            elif timed_out == 1:
                try:
                    writer.close()
                except Exception as e:
                    libs.logging.error(e)
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
                        object.status = "200"
                        object.FILES = request_object.FILES
                        object.temp = request_object.temp
                        object.headers = request_object.headers
                        # set needed headers for response
                        object.response_headers["Date"] = str(libs.Date.httpdate())
                        object.response_headers["Server"] = str(config.config.SERVER)
                        object.response_headers["Last-Modified"] = str(libs.Date.httpdate())
                        object.response_headers["Connection"] = "Closed"
                        page_content = handle_request(object)
                        DATA = libs.create_http.create(page_content)
                        writer.write(DATA)
                        await writer.drain()
                        writer.close()
                        
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
        try:
            log_info(page_content[1],time_took,address,request_full_url,dateandtime)
        except Exception as e:
            print(e)
        keys = list(page_content[1].FILES.keys())
        for x in range(len(keys)):
            try:
                os.remove(f"{config.config.TEMP}/{page_content[1].FILES[keys[x]]['temp']}")
            except:
                pass

        return 0
    except Exception as e:
        print(e)
        writer.close()
        libs.logging.error("A error has occured while handling request\n")
        

def server_main():
    try:
        loop = asyncio.get_event_loop()
        loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(config.config.ASYNCIO_MAX_WORKERS))
        loop.create_task(asyncio.start_server(handle_client, HOST, PORT))
        loop.run_forever()
    except OSError as sock_error:
        if sock_error.errno == 98:
            libs.logging.error("Socket already in use. Exiting...\n")
            sys.exit(0)
    except KeyboardInterrupt:
        try:
            loop.close()
        except:
            pass
        libs.logging.good("\b\bShutting Down\n")
        sys.exit(0)

    except:
        libs.logging.error("A error has occured while creating server socket\n")



        
server_main()
