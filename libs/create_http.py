#cython: language_level=3
import libs.Date
import config.config
import libs.colors
import threading
import sys
import libs.lemon
def status_print(page_content):

    if page_content[4].status =="200":
        print(libs.colors.colors.fg.green+page_content[4].status+libs.colors.colors.reset)
    elif page_content[4].status == "404":
         print(libs.colors.colors.fg.red+"404"+libs.colors.colors.reset)
    elif page_content[4].status == "403":
        print(libs.colors.colors.fg.red+"403"+libs.colors.colors.reset)
    elif page_content[4].status == "500":
        print(libs.colors.colors.fg.red+"500"+libs.colors.colors.reset)
    else:
        print(page_content[4].status)

def create(page_content):
    threading.Thread(target=status_print,args=(page_content,)).start()
    cookie_string = ""
    if len(page_content[2]) > 0:
        cookie_string = f"\n{str(page_content[2])}"
    else:
        pass
    page_content_1 = ""
    try:
        page_content_1 = page_content[0].encode("utf-8")
    except (UnicodeDecodeError, AttributeError):
        page_content_1 = page_content[0]
    return f'HTTP/1.1 {page_content[4].status} OK\r\nDate: {str(libs.Date.httpdate())}\r\nServer: {str(config.config.SERVER)}\r\nLast-Modified: {str(libs.Date.httpdate())}\r\nContent-Length: {str(page_content[3])}\r\nContent-Type: {str(page_content[1])}{str(cookie_string)}\r\nConnection: Closed\r\n\r\n'.encode("utf-8",errors="ignore")+page_content_1
def create_error(message,error_code):
    return f'HTTP/1.1 {error_code} OK\nDate: {str(libs.Date.httpdate())}\nServer: {str(config.config.SERVER)}\nLast-Modified: {str(libs.Date.httpdate())}\nContent-Length: {str(len(message))}\r\nContent-Type: text/html\r\nConnection: Closed\r\n\r\n{message}'.encode("utf-8")
