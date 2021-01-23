import json
import os
import importlib.util



def import_module_by_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class extensions:
    def __init__(self, extensions_list):
        with open(extensions_list,"r") as file:
            self.extensions = json.load(file)
    def cgi(self,ext,file,object):
        import_lib = f"lemon/extensions/{self.extensions['cgi'][ext][list(self.extensions['cgi'][ext])[0]]['location']}/{self.extensions['cgi'][ext][list(self.extensions['cgi'][ext])[0]]['extension-main-file']}"
        module = import_module_by_path(import_lib)
        return module.main().cgi(file,object)
    def check_cgi(self,ext):
        if str(ext) in self.extensions["cgi"]:
            return True
        else:
            return False


