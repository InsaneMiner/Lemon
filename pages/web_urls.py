import libs.request
import libs.RenderPage
import libs.redirect
import libs.file

def main(object):
    
    return libs.RenderPage.Render(object,"default.html",{"message":"Hello"})
    