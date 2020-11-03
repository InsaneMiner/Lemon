





def HttpOutput(object,output,_type,size):
    Cookies = object.new_cookies
    if size == "None":
        size = len(output)
    else:
        pass
    cookies1 = ""
    for key in Cookies.keys():
        cookies1 += "Set-Cookie: "+key+"="+Cookies[key]+";\n"
    if cookies1 == "":
        pass
    else:
        cookies1 = cookies1.rstrip("\n")
    return [output,_type,cookies1,size,object]
