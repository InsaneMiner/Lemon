import libs.RenderPage
import config.config
# this will have some good info https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
'''
This file will tell what the http status page will look like.
'''
v404 = "404 page not found" 
v500 = "500 Internal server error"
v403 = "403 error"
def e404(object):
    content = libs.RenderPage.RenderPath(object,config.config.errorHtmlFile,{"error_code":"404","error_content":v404})
    return content

def e500(object):
    content = libs.RenderPage.RenderPath(object,config.config.errorHtmlFile,{"error_code":"500","error_content":v500})
    return content

def e403(obejct):
    content = libs.RenderPage.RenderPath(object,config.config.errorHtmlFile,{"error_code":"403","error_content":v403})
    return content



