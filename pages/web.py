import libs.lemon


import socket
def connect_data(q):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("",9711))
    sock.sendall(bytes(q.lower(),"utf-8"))
    data = sock.recv(6003).decode("utf-8")
    sock.close()
    return data
def search_form(value):
    html = """
<form action="/search/" method="GET">
<h1><span style="color:yellow;display:inline;">A</span><span style="color:blue;display:inline">sk</span><span style=" color:green;display:inline;">Me</span><span style="color:yellow;display:inline;">!</span></h1>
<input id="query" style="width:500px;height:40px;border-radius:5px;border:solid 1px black;" type="text" name="q" value="%s">
<input type="submit" value="Search">
</form>
""" % value
    return html

def html(object):
    return HttpResponse(object,search_form(""),"text/html", "None")

def index(object):
    query = request.GET["q"]
    if query == None:
        return libs.lemon.HttpOutput(object,str(search_form("")),"text/html", "None")
    else:
        url_data = str(connect_data(query.lower()))
        if len(url_data) > 0: 
            return libs.lemon.HttpOutput(object,str(search_form(query))+"<br><hr size='1' style='color:#d3d3d3;'>"+url_data,"text/html", "None")
        else:
            return libs.lemon.HttpOutput(object,str(search_form(query))+"<br><hr size='1' style='color:#d3d3d3;' ><h1>Sorry No Results...</h1>","text/html", "None")




