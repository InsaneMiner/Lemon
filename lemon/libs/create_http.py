#cython: language_level=3
import lemon.libs.Date
import config.config
import lemon.libs.colors
import threading
import sys
import lemon.libs.lemon






HTTP_STATUS_CODES = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",  # see RFC 8297
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi Status",
    208: "Already Reported",  # see RFC 5842
    226: "IM Used",  # see RFC 3229
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",  # unused
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",  # unused
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",  # see RFC 2324
    421: "Misdirected Request",  # see RFC 7540
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",  # see RFC 8470
    426: "Upgrade Required",
    428: "Precondition Required",  # see RFC 6585
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    449: "Retry With",  # proprietary MS extension
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",  # see RFC 2295
    507: "Insufficient Storage",
    508: "Loop Detected",  # see RFC 5842
    510: "Not Extended",
    511: "Network Authentication Failed",
}










def status_print(page_content):

    if page_content[1].status =="200":
        print(lemon.libs.colors.colors.fg.green+page_content[1].status+lemon.libs.colors.colors.reset)
    elif page_content[1].status == "404":
         print(lemon.libs.colors.colors.fg.red+"404"+lemon.libs.colors.colors.reset)
    elif page_content[1].status == "403":
        print(lemon.libs.colors.colors.fg.red+"403"+lemon.libs.colors.colors.reset)
    elif page_content[1].status == "500":
        print(lemon.libs.colors.colors.fg.red+"500"+lemon.libs.colors.colors.reset)
    else:
        print(page_content[1].status)

def create(page_content):
    threading.Thread(target=status_print,args=(page_content,)).start()
    object = page_content[1]


    page_content_1 = ""
    try:
        page_content_1 = page_content[0].encode("utf-8")
    except (UnicodeDecodeError, AttributeError):
        page_content_1 = page_content[0]
    http_headers = ""

    http_headers += f"HTTP/1.1 {object.status} {HTTP_STATUS_CODES[int(object.status)]}\r\n" 
    for x in object.headers.keys():
        http_headers += f"{x}: {object.headers[x]}\r\n"
    http_headers += "\r\n"
    return http_headers.encode("utf-8",errors="ignore")+page_content_1
    #return f'HTTP/1.1 {page_content[4].status} OK\r\nDate: {str(lemon.libs.Date.httpdate())}\r\nServer: {str(config.config.SERVER)}\r\nLast-Modified: {str(lemon.libs.Date.httpdate())}\r\nContent-Length: {str(page_content[3])}\r\nContent-Type: {str(page_content[1])}{str(cookie_string)}\r\nConnection: Closed\r\n\r\n'.encode("utf-8",errors="ignore")+page_content_1


def create_error(message,error_code):
    return f'HTTP/1.1 {error_code} OK\nDate: {str(lemon.libs.Date.httpdate())}\nServer: {str(config.config.SERVER)}\nLast-Modified: {str(lemon.libs.Date.httpdate())}\nContent-Length: {str(len(message))}\r\nContent-Type: text/html\r\nConnection: Closed\r\n\r\n{message}'.encode("utf-8")
