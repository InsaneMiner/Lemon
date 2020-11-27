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
    return data1