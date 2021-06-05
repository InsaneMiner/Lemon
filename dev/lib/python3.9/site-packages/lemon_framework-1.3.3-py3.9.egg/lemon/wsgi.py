from urllib.parse import urlparse, urljoin, parse_qsl, parse_qs
import string
import random
import threading
import urllib.parse

import lemon.libs.multipart_formdata as mf
import lemon.libs.HttpObject
import lemon.libs.http_status as http_status
import lemon.libs.Date as Date

import lemon.libs.route



#Libs from user project
import app.urls
import config.config


sessions_  = {}




def current_cookies(Cookies):
    output = Cookies
    output = output.split(";")
    cookie = {}
    for x in range(len(output)):
        ex = output[x].split("=")
        if x > 0:
            cookie[ex[0][1:]] = ex[1]
        else:
            cookie[ex[0]] = ex[1]
    cookie[(list(cookie)[-1])] = cookie[(list(cookie)[-1])]
    return cookie






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


def get_page(object):
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
    
    data =  lemon.libs.route.page(object)
    threading.Thread(target=reset_session,args=(data,id_)).start()
    return data







def delete_all_temp_files(boject):
    keys = list(object.FILES.keys())
    for x in range(len(keys)):
        try:
            os.remove("{}/{}").format(config.config.TEMP,object.FILES[keys[x]]['temp'])
        except:
            pass











def Handle(env):

    _GET = {}
    FILES = {}
    _POST= {}
    Temp = {}
    COOKIES = {}
    # The request method
    REQUEST_METHOD = env["REQUEST_METHOD"]
    # This gets the requested path
    PATH = env["PATH_INFO"]
    try:
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    #This gets all the multipart/form-data if the request is that type
    request_body = env['wsgi.input'].read(request_body_size)
    try:
        if env["REQUEST_METHOD"].lower() == "post" and "multipart/form-data;" in env["CONTENT_TYPE"]:
            multipart_files = mf.multipart_formdata( b"Content-Type: " + env["CONTENT_TYPE"].encode("utf-8") + b"\r\nMIME-Version: 1.0\r\n\r\n" + request_body , config.config.TEMP, compile=False)
            data = request_body.decode("utf-8",errors="ignore").split("--"+env["CONTENT_TYPE"].replace("multipart/form-data; boundary=","",1))[:-1]
            for x in range(len(data)):
                if data[x] == "":
                    pass
                else:
                    if "=" in data[x]:
                        if "filename=" in data[x]:

                            name = data[x].split("\n")[1].split(";")[1].split("=")[1][1:-1]
                            if data[x].split("\n")[1].split(";")[1].split("=")[1][1:-1] == "\r":
                                name = name[:-1]

                            filename = data[x].split("\n")[1].split(";")[2][1:].split("=")[1][1:-1]
                            if data[x].split("\n")[1].split(";")[2][1:].split("=")[1][-1] == "\r":
                                filename = filename[:-1]
                            

                            

                            if name in multipart_files:
                                temp_file = multipart_files[name]["temp"]
                                file_content  = multipart_files[name]["content"]
                                file_type = multipart_files[name]["content_type"]
                            else:
                                file_type = None
                                file_content = ""


                            Temp[temp_file] = name
                            FILES[name] = {"name":filename,"content":file_content,"temp":temp_file,"type":file_type}
                        else:
                            name = data[x].split("\n")[1].split(";")[1].split("=")[1][1:-1]
                            if data[x].split("\n")[1].split(";")[1].split("=")[1][1:-1].endswith("\r\n"):
                                name = name[:-1]
                            file_content = data[x].split("\r\n")[3]

                            _POST[name[:-1]] = file_content
                            
                    else:
                        pass
        else:
            pass
    except Exception as e:
        print(e)
        
    # This will get all the post data from the enviroment variable
    if env["REQUEST_METHOD"].lower() == "post" and "multipart/form-data;" not in env["CONTENT_TYPE"]:
        _POST = parse_qs(request_body)
    # This will get all the cookies if there is any. Failing to do something is faster then checking if it exists. 
    # So this trying and excepting is faster
    try:
        COOKIES = current_cookies(env["HTTP_COOKIE"])
    except:
        pass
    # This will get the GET data from.
    try:
        _GET = parse_qs(env["QUERY_STRING"])
    except:
        pass

    request = lemon.libs.HttpObject.HttpObject(PATH,_GET, _POST,COOKIES,REQUEST_METHOD)

    request.FILES = FILES
    request.temp = Temp
    request.env = env


    # We need to set some headers for the response
    request.headers["Date"] = Date.httpdate()
    request.headers["Server"] = config.config.SERVER

    return request


def application(env, start_response):
    
    request = Handle(env)
    
    response_object = get_page(request)


    # get_page returns a list of two items. The first item is the stuff that wants to be sent to the client.
    # The second item is the request object.
    object = response_object[1]
    headers = []
    # Constructs all the headers into a list
    for x in object.headers.keys():
        headers.append(   (x, object.headers[x] )   )




   

    start_response(f"{object.status} {http_status.HTTP_STATUS_CODES[int(object.status)]}", headers)


    # This will run the function delete_all_temp_files in a thread. This function will delete all the files upload in the current request
    threading.Thread(target=delete_all_temp_files,args=(object)).start()
    # This must be a list. If it is a string it will send each letter one by one.
    # In other words it will iterate throught the string, that is why is must be a list.
    return [response_object[0]] 
