import pages.web_urls
import pages.errors
import config.config
import libs.RenderPage
import libs.colors













urls = {
    "/":"main"
    } 





































def page(object):
    if object.url in urls:
        try:
            data = getattr(pages.web_urls, urls[object.url])(object)
        except Exception as e:
            object.status = "500"
            data = pages.errors.e500(object)   
            print(e)
            
        return data
    else:
        try:
            data = libs.RenderPage.render_static(object,object.url[1:])
            return data
        except:
            object.status="404"
            return pages.errors.e404(object)
    
