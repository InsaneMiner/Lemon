## HOST and PORT info
HOST = "127.0.0.1"
PORT = 8000

## Server name
SERVER = "Lemon Server"


## folder config
STATIC = "static"
RENDER = "render"

## Token info for sessions
token = "SessionToken"
token_length = 100


#blacklist
blacklist = []

#Temp Folder
TEMP = "Temp"


#File extension for files that can have variables in them
FILE_EXTENSION_VAR = ".html"



errorHtmlFile = "config/error.html"

DEFAULT_MIME_TYPE = "text/plain"


LOG_LOCATION  = "app/log/log.txt"





ALLOWED_HOSTS = ["localhost","127.0.0.1"]



EXTENSIONS_CONFIG = "app/extensions/config.json"





# These are for the dev server

SOCKET_BUFFER = 65536

NORMAL_SERVER = True


DEBUG = False

ASYNCIO_MAX_WORKERS = 1000



#These are for ssl in the dev server
SSL_CERT = "config/ssl/ssl.crt"

SSL_KEY = "config/ssl/ssl.key"

SSL = False

SSL_PORT = 4433



# This should be changed to True when using gunicorn. If your using something 
# else and its not working try setting this to False
RETURN_BYTES = True

# These configurations are for gunicorn

bind = HOST+":"+str(PORT)
workers = 1
worker_connections = 1000
keepalive = 2
