
import pages.web
import libs.errors
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
            data = libs.errors.error(object,500)   
            print(e)
        return data
    else:
        try:
            data = libs.lemon.render_static(object,object.url[1:])
            return data
        except:
            return libs.errors.error(object,404)
    
