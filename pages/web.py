import libs.lemon

def main(object):
    print(object.headers)
    return libs.lemon.Render(object,"default.html")