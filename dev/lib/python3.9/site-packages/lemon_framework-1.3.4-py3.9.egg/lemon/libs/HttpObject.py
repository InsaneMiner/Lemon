#cython: language_level=3
class HttpObject:
    def __init__(object,url,_GET,_POST,cookies,method):
        object.GET = _GET
        object.POST = _POST
        object.method = method
        object.url = url
        object.status = "200"
        object.cookies = cookies
        object.new_cookies = {}
        object.session = {}
        object.temp = {}
        object.FILES = {}
        object.sessionReset = False
        object.headers = {
            "Date": "",
            "Server": "", 
            "Content-Length" : "",
            "Content-Type": "",
            "Connection": "Closed", 
        }