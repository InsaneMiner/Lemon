#cython: language_level=3
import email.parser
import string
import random
def random_temp(length = 10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def multipart_formdata(data,temp_folder):


    try:
        dis = data.decode("utf-8","ignore")
    except (UnicodeDecodeError, AttributeError):
        try:
            del dis
        except:
            pass
        return "Must be Bytes"
    new_data = b""
    orign = data.decode("utf-8","ignore")
    headers = orign[:orign.find("\n\n")].split("\n")

    new_data += "".join(s for s in headers if "Content-Type: multipart/form-data;" in s).encode("utf-8")+b"\n\n"

    if new_data.decode("utf-8").endswith("\n\n\n\n"):
        new_data = new_data[:-2]


    new_data += data[orign.find("\r\n\r\n")+4:]

    msg = email.parser.BytesParser().parsebytes(new_data)
    files = {}
    for part in msg.get_payload():
        name = part.get_param('name', header='content-disposition')
        if "filename=\"" in name:
            dq = part.get_param('name', header='content-disposition').find("\"",1,len(name))
            name = name[:dq]

        temp_file  = random_temp()

        with open(f"{temp_folder}/{temp_file}","wb") as file:
            file.write(part.get_payload(decode=True))
        

        files[name] = {"content": part.get_payload(decode=True) , "temp":temp_file,"content_type":part.get_content_type()}
    return files
    