import libs.Date
import config.config
import libs.colors
import threading
import sys
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
    DATA = b'HTTP/1.1 '+page_content[4].status.encode("utf8")+b' OK\nDate: '+str(libs.Date.httpdate()).encode("utf-8")+ b'\nServer: '+str(config.config.SERVER).encode("utf-8")+ b'\nLast-Modified: '+str(libs.Date.httpdate()).encode("utf-8")+ b'\nContent-Length: '+str(page_content[3]).encode("utf-8")+ b'\nContent-Type: '+str(page_content[1]).encode("utf-8")+str(cookie_string).encode("utf-8")+ b'\nConnection: Closed\n\n'+page_content_1
    return DATA