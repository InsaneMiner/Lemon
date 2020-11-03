import pages.web_urls
import pages.errors
import config.config
import libs.RenderPage
import libs.colors














urls = {
    "/":"main",
    "/hacker":"hacker",
    "/hacker/":"hacker"
    } 





































def page(object):
    if object.url in urls:
        try:
            data = getattr(pages.web_urls, urls[object.url])(object)
        except Exception as e:
            object.status = "500"
            data = libs.request.HttpOutput(object,pages.errors.e500(),"text/html","None")   
            print(e)
            
        return data
    else:
        try:
            data = libs.RenderPage.render_static(object,object.url[1:])
            return data
        except:
            object.status="404"
            return libs.request.HttpOutput(object,pages.errors.e404(),"text/html","None")
    
