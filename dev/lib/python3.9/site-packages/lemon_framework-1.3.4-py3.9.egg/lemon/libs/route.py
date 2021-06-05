import app.web
import lemon.libs.errors
import config.config
import lemon.libs.lemon
import lemon.libs.colors
import lemon.libs.url_validation
import app.urls


def page(object):
    correct_url = lemon.libs.url_validation.validate_url(object.url,app.urls.urls)
    if correct_url[0] != None:
        try:
            object.url_data = correct_url[1]
            data = getattr(app.web, app.urls.urls[correct_url[0]])(object)
        except Exception as e:
            data = lemon.libs.errors.error(object,500)   
            print(e)
        return data
    else:
        try:
            data = lemon.libs.lemon.render_static(object,object.url[1:])
            return data
        except:
            return lemon.libs.errors.error(object,404)