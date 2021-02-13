## This file creates a new project. 
# Usage: lemon-create.py project-name

from shutil import copyfile
import sys
import os
import lemon.path
import zipfile

if len(sys.argv) < 2:
    print("Usage: lemon-create.py project-name")  
else:
    copyfile(os.path.split(lemon.path.__file__)[0] + "/default.zip", sys.argv[1]+".zip")
    with zipfile.ZipFile(sys.argv[1]+".zip","r") as zip_ref:
        zip_ref.extractall(sys.argv[1])
    try:
        os.remove(sys.argv[1]+".zip")
    except:
        pass
    
    
