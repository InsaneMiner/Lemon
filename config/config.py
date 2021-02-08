
## HOST and PORT info
HOST = ""
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



errorHtmlFile = "lemon/error.html"

DEFAULT_MIME_TYPE = "text/plain"


LOG_LOCATION  = "lemon/log.txt"


SOCKET_BUFFER = 65536


ALLOWED_HOSTS = ["localhost","127.0.0.1"]



EXTENSIONS_CONFIG = "lemon/extensions/config.json"




USER_MODULE_PATH = "lemon/user/libs/"



NORMAL_SERVER = True


DEBUG = True

ASYNCIO_MAX_WORKERS = 1000




SSL_CERT = "lemon/ssl/ssl.crt"

SSL_KEY = "lemon/ssl/ssl.key"

SSL = False

SSL_PORT = 4433