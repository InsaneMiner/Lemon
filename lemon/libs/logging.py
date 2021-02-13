import lemon.libs.colors
def error(message,end=''):
    print(f"{lemon.libs.colors.colors.bold}{lemon.libs.colors.colors.fg.red}{message}{lemon.libs.colors.colors.reset}",end=end)
def good(message,end=''):
    print(f"{lemon.libs.colors.colors.fg.green}{message}{lemon.libs.colors.colors.reset}",end=end)
def notice(message,end=''):
    print(f"{lemon.libs.colors.colors.bold}{lemon.libs.colors.colors.fg.yellow}{message}{lemon.libs.colors.colors.reset}",end=end)
def log(message,end=''):
    print(message,end=end)