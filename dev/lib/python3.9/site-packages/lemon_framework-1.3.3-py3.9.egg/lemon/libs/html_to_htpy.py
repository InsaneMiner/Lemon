#cython: language_level=3
import re
def convert_to(text,variables = {}):
    data = re.findall('\{{([^}]+)\}}',  text)
    data1 = text
    for dat in data:
        if dat in variables:
            data1 = re.sub("{{"+re.escape(dat)+"}}",variables[dat],data1)
        else:
            pass
    return inl(data1)
def file_exists(file):
    try:
        open(file)
        return True
    except:
        return False
def html_file(file):
    with open(file,"r") as file:
        data = file.read()
    return data
def inl(text):
    data = re.findall('\{% include \"([^}]+)\" \%}',  text)
    data1 = text
    for dat in data:
        if file_exists(dat):
            data1 = re.sub("{% include \""+re.escape(dat)+"\" %}",html_file(dat),data1)

    return data1
