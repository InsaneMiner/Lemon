import subprocess
import os.path
import importlib.util
import sys


def import_module_by_path(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class stdout_stream():
    def __init__(self):
        self.var = ""
    def write(self,new_data):
        self.var += new_data
    def flush(self):
        pass
    def close(self):
        pass






class main():
    

    def cgi(self,file,object):

        try:

            open(file)

        except Exception as e:

            return b"File can't be found"

        sys.__stdout__ = sys.stdout


        self.stdout_stream = stdout_stream()

        sys.stdout = self.stdout_stream



        python_script = import_module_by_path(file)

        try:
            python_script.main

        except NameError:

            pass

        else:

            python_script.main(object)

        sys.stdout.close()


        sys.stdout = sys.__stdout__

        return (self.stdout_stream.var).encode("utf-8")