#cython: language_level=3
import config.config
import random
import string
import codecs
import lemon.libs.multipart_formdata
def get_random_string(length = 10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def multipart_form_data(http,raw_http):
    data = ""
    foundFiles = False
    boundry = ""
    Temp = {}
    _POST= {}
    FILES = {}

    multipart_files = lemon.libs.multipart_formdata.multipart_formdata(raw_http,config.config.TEMP)
    for line in http.splitlines():
        if foundFiles:
            data += line+"\n"
        if line.startswith("Content-Type: "):
            if foundFiles:
                pass
            else:
                boundry = line.replace("Content-Type:","",1).replace("multipart/form-data;","",1).replace(" ","").replace("boundary=","",1)
                foundFiles = True
    data = http.split("\r\n\r\n",1)[1]
    headers = http.split("\r\n",1)[0]
    data = data.split("--"+boundry)[:-1]
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
            



    headers_dict = {}
    x_ = 0
    for line in headers.splitlines():
        if x_ == 0:
            pass
        else:
            if line == "":
                pass
            else:
                headers_dict[line.split(":",1)[0]] = line.split(":",1)[1][1:]
        x_ += 1
    return headers_dict,Temp,FILES, _POST