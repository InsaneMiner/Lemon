## Manual

How to add items to session:<br>
object.session["item_name"] = "var"
<br>
How to add new cookies:<br>
object.new_cookies["item_name"] = "var"
<br>
How to get session data:<br>
var = object.session["item_name"]
<br>
How to get cookies:<br>
var = object.cookies["item_name"]
<br>
How to get Post request data:<br>
var = object.POST["item_name"]
<br>
How to get Get request data:<br>
var = object.GET["item_name"]
<br>
How to get request method:<br>
var = object.method
<br>
How to get current url:<br>
var = object.url
<br>
How to render pages in render folder:<br>
import libs.RenderPage<br>
return libs.RenderPage.Render(object,"file.file")<br>
If you want to add variables to html files then add {{variable}}<br>
then return:<br>
return libs.RenderPage.Render(object,"file.file",{"variable":"hello"})
<br>
How to display custom text from python:<br>
import libs.request<br>
return libs.request.HttpOutput(object,"     <html><head></head><body><h1>Hello<h1></body></html>    ","text/html","None")
<br>
How to change port number:<br>
change the PORT variable in the config/config.py file.
<br>
Change the Server name:<br>
Change the SERVER variable in the config/config.py file.
<br>
How to change the static folder:<br>
Change the STATIC variable in the config/config.py file, to a folder name that exists that you want.
<br>
How to change the render folder:<br>
Change the RENDER variable in the config/config.py file, to a folder name that exists that you want.
<br>
How to change the length of the token that can be generate:<br>
Change the token_length variable in the config/config.py file, to a valid integer.
<br>
How to redirect to another page:<br>
import libs.redirect<br>
return libs.redirect.redirect(object,"/url")
<br>

### WARNINGS:<br>
 - Please do not change the HOST variable in the config/config.py file unless you know what it does.

<br>
When importing files you have to import them as you are in the main.py file.
