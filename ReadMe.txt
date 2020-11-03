MANUAL
How to add items to session:
object.session["item_name"] = "var"

How to add new cookies:
object.new_cookies["item_name"] = "var"

How to get session data:
var = object.session["item_name"]

How to get cookies:
var = object.cookies["item_name"]

How to get Post request data:
var = object.POST["item_name"]

How to get Get request data:
var = object.GET["item_name"]

How to get request method:
var = object.method

How to get current url:
var = object.url

How to render pages in render folder:
import libs.RenderPage
return libs.RenderPage.Render(object,"file.file")
If you want to add variables to html files then add {{variable}}
then return:
return libs.RenderPage.Render(object,"file.file",{"variable":"hello"})

How to display custom text from python:
import libs.request
return libs.request.HttpOutput(object,"<html><head></head><body><h1>Hello<h1></body></html>","text/html","None")

How to change port number:
change the PORT variable in the config/config.py file.

Change the Server name:
Change the SERVER variable in the config/config.py file.

How to change the static folder:
Change the STATIC variable in the config/config.py file, to a folder name that exists that you want.

How to change the render folder:
Change the RENDER variable in the config/config.py file, to a folder name that exists that you want.

How to change the length of the token that can be generate:
Change the token_length variable in the config/config.py file, to a valid integer.

How to redirect to another page:
import libs.redirect
return libs.redirect.redirect(object,"/url")

WARNINGS:
1. Please do not change the HOST variable in the config/config.py file unless you know what it does.


When importing files you have to import them as you are in the main.py file.