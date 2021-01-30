
import pages.web
import pages.errors
import config.config
import libs.lemon
import libs.colors
import libs.url_validation












urls = {
    "/":"main",
    } 





































def page(object):
    correct_url = libs.url_validation.validate_url(object.url,urls)
    if correct_url[0] != None:
        try:
            object.url_data = correct_url[1]
            data = getattr(pages.web, urls[correct_url[0]])(object)
        except Exception as e:
            object.status = "500"
            data = pages.errors.e500(object)   
            print(e)
        return data
    else:
        try:
            data = libs.lemon.render_static(object,object.url[1:])
            return data
        except:
            object.status="404"
            return pages.errors.e404(object)
    
