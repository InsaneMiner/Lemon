#cython: language_level=3

#Do not change anything unless you know what your doing. It could brake the whole thing
import config.config
HOST = config.config.HOST
PORT = config.config.PORT
SERVER = config.config.SERVER
import libs.Date
import socket
import libs.lemon
import libs.create_http
import pages.urls
import libs.HttpObject
import libs.handleHttp
import libs.colors
import libs.logging
import base64, asyncio, re, time, string, random, sys, threading, os, concurrent.futures
import cProfile, pstats

try:
    import ssl
except:
    libs.logging.error("No ssl")

sessions_  = {}



def get_random_string(length=config.config.token_length):
    """
    
    This function just generates a random token. 
    This token is a random string.

    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def reset_session(data,id_):
    """

    This function resets the current clients session.

    """
    global sessions_
    if data[1].sessionReset:
        sessions_ = sessions_.pop(id_)
    else:
        sessions_[id_] = data[1].session


def handle_request(object):
    """

    This takes in the request object. The request object has info 
    like url that is requested, cookies, files that have been uploaded, 
    headers and more. This function will use this request object, and find 
    the app code for the url that has been requested by the client.
    It will also make sure the client has a session id. If the client does 
    not have a session id it will asign the client with one. It will also reset all 
    session data if told to.

    """
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
    """

    This will log the request info. This will log the time it took to handle the request and some more info. 
    
    """

    with open(config.config.LOG_LOCATION,"a+") as log_file:
        log_file.write(f"TIMETOOK[{time_took}] DATE&TIME[\"{dateandtime}\"] IP[{address[0]}] URL[\"{object.url}\"] REQUEST[\"{request_full_url}\"] STATUS[{object.status}]\n")


# Content-Type header: Content\-Type\:\smultipart/form\-data\;\sboundary\=(.*?)\n$
 

async def handle_client(reader,writer):
    """

    This function handles the client.
    The slowest part of this function is receiving the request. 
    The hard part of receiving multi-part/formdata is it needs 
    to find the end of the request. This can be hard and slow 
    when the file is large.


    """
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
            #stats.print_stats()
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
            time_message = "{}{}{}".format(libs.colors.colors.fg.red, time_took,libs.colors.colors.reset)
        else:
            time_message = "{}{}{}".format(libs.colors.colors.fg.green,time_took,libs.colors.colors.reset)
    
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
                os.remove("{}/{}").format(config.config.TEMP,page_content[1].FILES[keys[x]]['temp'])
            except:
                pass

        return 0
    except Exception as e:
        print(e)
        writer.close()
        libs.logging.error("A error has occured while handling request\n")







def start_non_ssl_server():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        """
        Sets the asyncio workers to the value of config.config.ASYNCIO_MAX_WORKERS. 
        The default value is 1000. so the default workers is 1000.
        """
        loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(config.config.ASYNCIO_MAX_WORKERS))
        """
        Starts the http server.
        """
        loop.create_task(asyncio.start_server(handle_client, HOST, PORT))
        """
        this makes the server run forever
        """
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except OSError as sock_error:
        if sock_error.errno == 98:
            libs.logging.error("Socket already in use. Exiting...\n")
            sys.exit(0)
    except Exception as e:
        libs.logging.error("A error has occured while creating server socket\n")
        libs.logging.log(e)

def start_ssl_server(ssl_context):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        """
        Sets the asyncio workers to the value of config.config.ASYNCIO_MAX_WORKERS. 
        The default value is 1000. so the default workers is 1000.
        """
        loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(config.config.ASYNCIO_MAX_WORKERS))
        """
        Starts the http server.
        """
        loop.create_task(asyncio.start_server(handle_client, HOST, config.config.SSL_PORT, ssl= ssl_context))
        """
        this makes the server run forever
        """
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except OSError as sock_error:
        if sock_error.errno == 98:
            libs.logging.error("Socket already in use. Exiting...\n")
            sys.exit(0)
    except Exception as e:
        libs.logging.error("A error has occured while creating server socket\n")
        libs.logging.log(e)
def server_main():
        if config.config.NORMAL_SERVER:
            try:
                normal_thread = threading.Thread(target=start_non_ssl_server)
                normal_thread.daemon=True
                normal_thread.start()
            except KeyboardInterrupt:
                sys.exit(0)
            except OSError as sock_error:
                if sock_error.errno == 98:
                    libs.logging.error("Socket already in use. Exiting...\n")
                    sys.exit(0)
            except Exception as e:
                libs.logging.error("A error has occured while creating server socket\n")
                libs.logging.log(e)
        if config.config.SSL:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.check_hostname = False
            ssl_context.load_cert_chain(config.config.SSL_CERT, config.config.SSL_KEY)
            try:
                ssl_thread = threading.Thread(target=start_ssl_server, args=(ssl_context,))
                ssl.daemon=True
                ssl_thread.start()
            except KeyboardInterrupt:
                sys.exit(0)
            except OSError as sock_error:
                if sock_error.errno == 98:
                    libs.logging.error("Socket already in use. Exiting...\n")
                    sys.exit(0)
            except Exception as e:
                libs.logging.error("A error has occured while creating server socket\n")
                libs.logging.log(e)



server_main()


