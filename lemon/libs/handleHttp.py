#cython: language_level=3
import urllib.parse
import lemon.libs.form_handle
import codecs
import re
def split_header(h):
    return h.split(": ",1)
def current_cookies(Cookies):
    output = Cookies[8:]
    output = output.split(";")
    cookie = {}
    for x in range(len(output)):
        ex = output[x].split("=")
        if x > 0:
            cookie[ex[0][1:]] = ex[1]
        else:
            cookie[ex[0]] = ex[1]
    cookie[(list(cookie)[-1])] = cookie[(list(cookie)[-1])][:-1]
    return cookie
class RequestObject:
    def __init__(self):
        page=""
        cookies = {}
        headers = []
        url = ""
        _POST = {}
        _GET = {}
        request_type = ""
def get_headers(request):
    headers = request.decode("utf-8","ignore").split("\r\n\r\n",1)[0]
    headers_dict = {}
    x_ = 0
    for line in headers.splitlines():
        if x_ == 0:
            pass
        else:
            if ":" not in line:
                break
            headers_dict[line.split(":",1)[0]] = line.split(":",1)[1][1:]
        x_ += 1
    return headers_dict
def http(headers):
    headers1 = headers
    headers = headers.decode("utf-8","ignore").split("\n")
    _POST={}
    url = headers[0]
    if len(headers) > 8:
        cookies  = "".join(s for s in headers if "Cookie:" in s)
        if "Cookie" in cookies:
            is_cookie = True
        else:
            is_cookie = False
    else:
        is_cookie = False
    request_type = re.findall(r"([\w]{1,})\s",url)[0]
    if request_type == "GET":
        url = url.replace(url[:3], '')
        headers_ = {}
        Temp = {}
        FILES = {}
    elif request_type == "POST":
        url = url.replace(url[:4],"")
        current_headers = get_headers(headers1)
        if "Content-Type" in current_headers:
            if "multipart/form-data;" in current_headers["Content-Type"]:
                headers_ , Temp , FILES , _POST1= lemon.libs.form_handle.multipart_form_data(headers1.decode("utf-8","ignore"),headers1)
                _POST.update(_POST1)
            else:
                headers_ = {}
                Temp = {}
                FILES = {}
        else:
            headers_ = {}
            Temp = {}
            FILES = {}
    else:
        headers_ = {}
        Temp = {}
        FILES = {}
    HTTP_VERSION  = re.findall(r"(HTTP)/([0-9]\.[0-9])",url)
    url = url.replace(f"HTTP/{HTTP_VERSION[0][1]}","",1)
    url = url.replace(" ","")
    if "?" in url:
        url_parts = url.split("?")
        page = url_parts[0]
    else:
        url = url.replace("\r","")
        page = url
    _GET = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    _POST1 = headers[len(headers)-1].split("&")
    for x in range(len(_POST1)):
        try:
            _POST[_POST1[x].split("=")[0]] = _POST1[x].split("=")[1]
        except:
            pass
    if _GET == {}:
        pass
    else:
        _GET[(list(_GET)[-1])] = _GET[(list(_GET)[-1])][:-1]
    if is_cookie:
        pass
    else:
        cookies = {}
    if cookies == {}:
        pass
    else:
        cookies = current_cookies(cookies)
    page = page.replace("../","").replace("./","")
    new_headers = list(map(split_header, headers))
    headers = {}
    for h in new_headers:
        if len(h) > 1:
            headers[h[0]] = h[1]
        else:
            pass
    object = RequestObject()
    object.POST = _POST
    object.GET = _GET
    object.cookies = cookies
    object.url = url
    object.page = page
    object.headers = headers
    object.request_type = request_type
    object.temp = Temp
    object.FILES = FILES
    object.HTTP_VERSION = HTTP_VERSION[0][1]
    return object
