import os
import libs.request
import pages.errors
import libs.file_extensions
import os.path
import config.config
import libs.colors
import libs.html_to_htpy
import random
import string
import threading



def ext(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension












def render_static(object,file):
    try:
        with open(f"{config.config.STATIC}/{file}","rb") as fo:
            content = fo.read()
        file_size = os.path.getsize(f"{config.config.STATIC}/{file}")
        if ext(file) in libs.file_extensions.extensions:
            return libs.request.HttpOutput(object,content,libs.file_extensions.extensions[ext(file)],file_size)
        else:
            return libs.request.HttpOutput(object,content,"text/plain",file_size)
    except PermissionError:
        object.status = "403"
        return pages.errors.e403(object)
    except (IsADirectoryError,FileNotFoundError):
        object.status = "404"
        return pages.errors.e404(object)
    except Exception as e:
        print(e)
        object.status = "500"
        return pages.errors.e500(object)



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
            return libs.request.HttpOutput(object,content,libs.file_extensions.extensions[ext(file)],file_size)
        else:
            return libs.request.HttpOutput(object,content,"text/plain",file_size)
    except PermissionError:
        object.status = "403"
        return pages.errors.e403(object)
    except FileNotFoundError:
        object.status = "404"
        return pages.errors.e404(object)
    except Exception as e:
        print(e)
        object.status = "500"
        return pages.errors.e500(object)


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
            return libs.request.HttpOutput(object,content,libs.file_extensions.extensions[ext(file)],file_size)
        else:
            return libs.request.HttpOutput(object,content,"text/plain",file_size)
    except PermissionError:
        object.status = "403"
        return pages.errors.e403(object)
    except FileNotFoundError:
        object.status = "404"
        return pages.errors.e404(object)
    except Exception as e:
        print(e)
        object.status = "500"
        return pages.errors.e500(object)