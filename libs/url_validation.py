import re
def check_for_parameters(text):
    data = re.findall('\<([^}]+)\>',  text)
    data1 = text
    return "".join(data)
def validate_url(inputed_url,url_list):
    url_data,same_url= {},0
    for url1 in url_list:
        url = url1
        input_url = inputed_url
        if len(url.split("/")) == len(input_url.split("/")):
            url,input_url = url.split("/"),input_url.split("/")
            for x in range(len(url)):
                if url[x] == input_url[x]: same_url=1
                else:
                    regex_output = check_for_parameters(url[x])
                    if regex_output == '':same_url = 0;url_data={} ;break
                    else: url_data[regex_output] = input_url[x];same_url=1           
        else:same_url = 0;url_data={};continue
        if same_url ==1:
            return [url1, url_data]
        else:
            continue
    return [None,{}]