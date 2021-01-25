import libs.colors
def error(message,end=''):
    print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.red}{message}{libs.colors.colors.reset}",end=end)
def good(message,end=''):
    print(f"{libs.colors.colors.fg.green}{message}{libs.colors.colors.reset}",end=end)
def notice(message,end=''):
    print(f"{libs.colors.colors.bold}{libs.colors.colors.fg.yellow}{message}{libs.colors.colors.reset}",end=end)
def log(message,end=''):
    print(message,end=end)