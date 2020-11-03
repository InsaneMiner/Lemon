request = """GET / HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1""".split('\n')

reqs = {}

for x in request:
    if "GET" in x:
        method, path, http = x.split(" ")
        reqs["REQUESTS"] = path
    else:
        key, val = x.split(": ")
        reqs[key] = val
