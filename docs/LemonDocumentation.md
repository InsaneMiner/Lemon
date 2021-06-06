# Lemon Documentation


### What is Lemon

Lemon is a web server and web framework written in python. Lemon is easy to start with, even if you are a beginner with python, you can create a website.

### Why Lemon was created

One day I was making a simple search engine, I just had finished the book Google it. I was inspired after reading the book, so I wanted to create a search engine. The only programming language a new enough of to write a search engine was python. I wanted it to work as a website, like Google. I thought of using flask because it was simple, but I did not really like how you had I had to write my application, Then I thought maybe django would be good, its got a good way of writing web application, I thought, but when I start writing the website, I found it was harder than it had to be. So I thought, how hard could it really be to write a web framework from scratch by my self, let me tell you it was not as easy as I thought, but in the end I did it. It took me 1-2 months. So that is why I created Lemon.

### What you need to know to get start

You will need to know basic HTML and CSS, for the front end. The backend is all written in python.

### Documentation

- Setting up Lemon
 
- Setting up a new project

- Displaying html onto a page

- Dispalying html file

- Display html file with variables aka templating

- Add more paths/urls.

- Creating basic "Hello World" website

- Redirecting to a another page

- Using POST and GET data

- File upload

- Using sessions

- Displaying html with variables

- Url Variables - unfixed urls

  
#### Installing with pip
With windows
```
pip install lemon-framework
```
On mac and linux
```
pip3 install lemon-framework
```
### Installing from source
download the source code with.

```

git clone https://github.com/InsaneMiner/Lemon.git

```

Then Enter your new directory with

```

cd Lemon

```
##### Now you to install all required packages
for Mac and Linux
```
pip3 install -r requirements
```
For Windows

```

pip install -r requirements.txt

```
##### Now you need to install lemon

for Mac and Linux
```

python3 setup.py install

```

For Windows

```

python setup.py install

```

Now Lemon is installed from source
### Setting up a new project

Once you have lemon installed you need to create your first project
##### Run these commands:
Windows
```
python -m lemon.lemonCreate project-name
```
Mac and Linux
```
python3 -m lemon.lemonCreate project-name
```
Now you should have a new directory with the name of your project, that is your project.
### Running the project
Running your new app is not that hard.<br>
#### Running with development server (For development).
Lemon has a built-in development server for testing and development.
To run this first enter the directory of your project
```
cd project-name
```
then run these commands
##### On windows
```
python main.py
```
#### On Mac and Linux
```
python3 main.py
```
#### Running the wsgi server(for production/public with small web apps)
This is needed when you want your app to go public because the built-in development server is slower and less secure (Please see development server issues section for more info). You could set it up with a web server like `apache` or `nginx`(I will talk a little more on this later), but I'm going to show you how to do it with `gunicorn`(more on gunicorn  [here](https://docs.gunicorn.org/en/stable/)). So first we need to install gunicorn.Please go [here](https://docs.gunicorn.org/en/stable/install.html) for info on installing it. Now enter the directory that the project is located in
```
cd project-name
```
then run 
```
python3 -m gunicorn wsgi -c config/config.py
```
There now your web app is running on the port you have configured it on.
#### Running with a real server (For production/public for big apps)(recommended for serious/big apps)
Gunicorn is really powerfull so you should not need this until your app is big or has lots of requests.
Im not going to teach you, but I'm going to give you some links to info that could help.
 - [https://modwsgi.readthedocs.io/en/develop/](https://modwsgi.readthedocs.io/en/develop/)
 - [https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html)
 - [https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04)
 - [https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html](https://uwsgi-docs.readthedocs.io/en/latest/Nginx.html)
 - [https://medium.com/analytics-vidhya/what-is-wsgi-web-server-gateway-interface-ed2d290449e](https://medium.com/analytics-vidhya/what-is-wsgi-web-server-gateway-interface-ed2d290449e)
 - [https://easycodeshare.com/wsgi-app-in-python-under-apache-mod_wsgi/](https://easycodeshare.com/wsgi-app-in-python-under-apache-mod_wsgi/)

### Displaying html onto a page

To display HTML onto a page with python we will need to add some code to a file. So know open the file in the **app** directory.

  

In that directory you should see these files and directories

```
urls.py

web.py

extensions

log
```

You need to edit the **web.py** file.

The default code in **web.py** file should be.

```python

import lemon.libs.lemon

  

def  main(object):

return lemon.libs.lemon.Render(object,"default.html")

```

To add your custom html you need to change the line

```python

return lemon.libs.lemon.Render(object,"default.html")

```

To

```python

return lemon.libs.lemon.HttpObject(object,"<h1>Hello World</h1>", "text/html", "None")

```

So this new code will dispaly Hello World onto the page. The **text/html** part is the mime type. This page should help with explaining mime types https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types. The **None** is there because it tells the size of the content. **None** Just tells Lemon it has to calculate the size itself.

  

### Dispalying html file

To display HTML pages is really easy.

All the files you are going to display are going to be in **render** directory.

So first create a file called **myfile.html** in the **render** directory.

Then add this code to **myfile.html**

```html

<h1>This is a simple html file</h1>

```

Then you need to edit the **web.py** file in the **pages** directory.

change the line

```python

return lemon.libs.lemon.Render(object,"default.html")

```

To

```python

return lemon.libs.lemon.Render(object,"myfile.html")

```

Then restart the server and then open it up in the browser.

All files that you are going to use render with are going to be in the **render** directory.

### Display html file with variables aka templating

Lemon uses jinja2 as a templating system.
here is some info on jinja2 syntax.
 - [https://docs.plextrac.com/plextrac-documentation/jinja-templating/jinja-basic-and-foundations/jinja-syntax](https://docs.plextrac.com/plextrac-documentation/jinja-templating/jinja-basic-and-foundations/jinja-syntax)
 - [https://docs.exponea.com/docs/jinja-syntax](https://docs.exponea.com/docs/jinja-syntax)

First we need to create a file called **myfile.html** in the **render** directory.

The code in myfile.html should look like

```html

<h1>{{ username }}</h1>

```

Then in the **web.py** you need to change the line

```python

return lemon.libs.lemon.render_template(object,"default.html")

```

To

```python

return lemon.libs.lemon.render_template(object,"myfile.html",username="Username")

```

Now open it up in the browser.

it should display **Username** in the browser. So that is how you can use variables in your html files. This also can work in css and javascript files.

### Add more paths/urls.

To add a new path you need to change a dictionary in the **urls.py**.

The **urls.py** is located in the **pages** directory.

The dictionary you need to change looks like

```python

urls = {

"/":"main"

}

```

To add a new path just add a new key.

for example i want to add a new page called **/blog**.

Then i would look like this

```python

urls = {

"/":"main",

"/blog":"blogfunction"

}

```

Now we need to make a function which will display the html code.

So edit the **web.py** file and add a new function with the name of blogfunction.

Then add a some code to that function so it will display the html code.

The page name can be anything but it must start with **/** and the function name can be anything to.

### Creating basic “Hello World” website

In the section we are going to make a basic website that you will be able to have many pages. So first we need to add a new **path**. The path is going to be **/mydog**, the function is going to be called mydog.

So once we have a new page we are going to display a image.

Now create a new html file in the **render** directory, called mydog.html.

The new file should have this code.

```html

<img  src="/mydog.png">

```

Now add a file called mydog.png into the **static** directory.

Now your **mydog** function should look like this

```python

def  mydog(object):
    return lemon.libs.lemon.render_template(object,"mydog.html")

```

So now if you restart the server and then open up the browser then type in

```

http://localhost:8000/mydog

```

Then it should display the image from your **static** directory.

### Redirecting to a another page

This can come in really handy when for example the user types in the wrong password and you want to redirect them to the failed login page.

So to do this you should change

```python

return lemon.libs.lemon.render_template(object,"default.html")

```

To

```python

return lemon.libs.lemon.redirect(object,"/url")

```

### Using POST and Get data

To access GET data use

```python

object.GET["nameofdata"]

```

To access POST data is almost the same as GET.

```python

object.POST["nameofdata"]

```

### File uploads

Use

```python

object.FILES["itemname"]

```

To change the location of this file really easy.

first import a lemon library with

```python

import lemon.libs.file

```

Then use

```python

lemon.libs.file.move_uploaded_file(object.FILES["itemname"]["temp"],"new/location/example.png")

```

### Using sessions

Session data is stored in a dictionary format.

So accessing it is really easy.

To set new session data use

```python

object.session["name"] = "something"

```

To access just use

```python

object.session["name"]

```

To reset the session use

```python

lemon.libs.lemon.ResetSession(object)

```

### Displaying html with variables

To display html with variables is like displaying html.

just use this instead

```python

return lemon.libs.lemon.HttpObjectVar(object,"<h1>Hello, {{name}}</h1>", "text/html", "None",{"name":"username"})

```

That is all thats needed.

  

### Url variables - unfixed urls

Url variables are data passed in through the url for example

```

/pages/dogs/beagles

```

and your url that you would set would look like

```

/pages/dogs/<dog_bread>

```

so to access the variables use

```python

object.url_data["dog_bread"]

```

so you could use this for passing info and it looks better than ?dog_bread=beagles