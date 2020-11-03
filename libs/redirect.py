import libs.request

def redirect(object,url):
    data = "<!DOCTYPE html>\n<html>\n<head><script>location.replace('"+url+"')</script></head>\n<body></body>\n</html>"
    print("redirecting:",object.url,"-->",url)
    return libs.request.HttpOutput(object,data,"text/html","None")
