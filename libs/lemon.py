#cython: language_level=3
import os
import libs.errors
import libs.file_extensions
import os.path
import config.config
import libs.colors
import libs.html_to_htpy
import random
import string
import threading
import libs.extensions
import sys

extensions = libs.extensions.extensions(config.config.EXTENSIONS_CONFIG)

def ext(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension.lower()
def render_static(object,file):
    try:
        if extensions.check_cgi(ext(file)):
            content = extensions.cgi(ext(file),f"{config.config.STATIC}/{file}",object)
            mime_type = extensions.extensions['cgi'][ext(file)][list(extensions.extensions['cgi'][ext(file)])[0]]['Mime-Type']
            file_size = sys.getsizeof(content)
        else:
            with open(f"{config.config.STATIC}/{file}","rb") as fo:
                content = fo.read()
            if ext(file) in libs.file_extensions.extensions:
                mime_type = libs.file_extensions.extensions[ext(file)]
            else:
                mime_type = config.config.DEFAULT_MIME_TYPE
            file_size = os.path.getsize(f"{config.config.STATIC}/{file}")
        return HttpOutput(object,content,mime_type,file_size)
       
    except PermissionError:
        return libs.errors.error(object,403)
    except (IsADirectoryError,FileNotFoundError):
        return libs.errors.error(object,404)
    except OSError as exc:
        if exc.errno == 36:
            return libs.errors.error(object,404)
    except Exception as e:
        print(e)
        return libs.errors.error(object,500)



def get_random_string(length=config.config.token_length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str






def Render(object,file,var={}):
    try:
        with open(f"{config.config.RENDER}/{file}","rb") as fo:
            content = fo.read()
        if ext(file) == config.config.FILE_EXTENSION_VAR:
            content = libs.html_to_htpy.convert_to(content.decode(),var).encode("utf-8")
            temper = True
        else:
            temper = False
        if temper:
            new_file_name = get_random_string()
            with open(f"{config.config.TEMP}/{new_file_name}","wb") as file11:
                file11.write(content)
            file_size = os.path.getsize(f"{config.config.TEMP}/{new_file_name}")
            threading.Thread(target=os.remove, args=(f"{config.config.TEMP}/{new_file_name}",)).start()
        else:
            file_size = os.path.getsize(f"{config.config.RENDER}/{file}")
        if ext(file) in libs.file_extensions.extensions:
            return HttpOutput(object,content,libs.file_extensions.extensions[ext(file)],file_size)
        else:
            return HttpOutput(object,content,config.config.DEFAULT_MIME_TYPE,file_size)
    except PermissionError:
        return libs.errors.error(object,403)
    except FileNotFoundError:
        return libs.errors.error(object,404)
    except Exception as e:
        print(e)
        return libs.errors.error(object,500)


def RenderPath(object,file,var={}):
    try:
        with open(f"{file}","rb") as fo:
            content = fo.read()
        if ext(file) == config.config.FILE_EXTENSION_VAR:
            content = libs.html_to_htpy.convert_to(content.decode(),var).encode("utf-8")
            temper = True
        else:
            temper = False
        if temper:
            new_file_name = get_random_string()
            with open(f"{config.config.TEMP}/{new_file_name}","wb") as file11:
                file11.write(content)
            file_size = os.path.getsize(f"{config.config.TEMP}/{new_file_name}")
            threading.Thread(target=os.remove, args=(f"{config.config.TEMP}/{new_file_name}",)).start()
        else:
            file_size = os.path.getsize(f"{file}")
        if ext(file) in libs.file_extensions.extensions:
            return HttpOutput(object,content,libs.file_extensions.extensions[ext(file)],file_size)
        else:
            return HttpOutput(object,content,config.config.DEFAULT_MIME_TYPE,file_size)
    except PermissionError:
        return libs.errors.error(object,403)
    except FileNotFoundError:
        return libs.errors.error(object,404)
    except Exception as e:
        print(e)
        return libs.errors.error(object,500)









def HttpOutput(object,output,_type,size):
    Cookies = object.new_cookies
    if size == "None":
        size = len(output)
    else:
        pass
    cookies1 = ""
    rotation = 1
    for key in Cookies.keys():
        if rotation == 1:
            if rotation == len(Cookies):
                cookies1 += f"{key}={Cookies[key]};"
            else:
                cookies1 += f"{key}={Cookies[key]};\r\n"

        else:
            
            if rotation == len(Cookies):
                cookies1 += f"Set-Cookie: {key}={Cookies[key]};"
            else:
                cookies1 += f"Set-Cookie: {key}={Cookies[key]};\r\n"
        rotation+=1
        
    if cookies1 == "":
        pass
    else:
        object.response_headers["Set-Cookie"] = cookies1
        cookies1 = cookies1.rstrip("\n")
    #set some headers
    object.response_headers["Content-Type"] = str(_type)
    object.response_headers["Content-Length"] = str(size)
    return [output,object]




def HttpOutputVar(object,output,_type,size,var={}):
    Cookies = object.new_cookies
    if size == "None":
        size = len(output)
    else:
        pass
    cookies1 = ""
    rotation = 1
    for key in Cookies.keys():
        if rotation == 1:
            if rotation == len(Cookies):
                cookies1 += f"{key}={Cookies[key]};"
            else:
                cookies1 += f"{key}={Cookies[key]};\r\n"

        else:
            
            if rotation == len(Cookies):
                cookies1 += f"Set-Cookie: {key}={Cookies[key]};"
            else:
                cookies1 += f"Set-Cookie: {key}={Cookies[key]};\r\n"
        rotation+=1


    if cookies1 == "":
        pass
    else:
        object.response_headers["Set-Cookie"] = cookies1
        cookies1 = cookies1.rstrip("\n")
    output = libs.html_to_htpy.convert_to(output,var).encode("utf-8")
    #set some headers
    object.response_headers["Content-Type"] = str(_type)
    object.response_headers["Content-Length"] = str(size)


    
    return [output,object]









def redirect(object,url):
    object.response_headers["Location"] = url
    object.status = "302"
    print("\nredirecting:",object.url,"-->",url)
    return HttpOutput(object,"","text/html","None")




def ResetSession(object):
    object.session = {}
    object.sessionReset = True
