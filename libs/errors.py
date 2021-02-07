import libs.lemon
import config.config
# this will have some good info https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
'''
This file will tell what the http status page will look like.
'''



HTTP_STATUS_MESSAGES = {
    404 : "404 page not found",
    500 : "500 Internal server error",
    403 : "403 error"
}


def error(object,error_code):
    object.status=str(error_code)
    return libs.lemon.RenderPath(object,config.config.errorHtmlFile,{"error_code":str(error_code),"error_content":HTTP_STATUS_MESSAGES[error_code]})









