#!/usr/bin/env python3

from setuptools import find_packages, setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import os, sys, time
import threading
import itertools
import shutil


def spin(msg, done): 
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))  
        if done.wait(.1):
            break
    write(' ' * len(status) + '\x08' * len(status))  



class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


os.chdir("libs/")



i = 0
dir_name = "."
test = os.listdir(dir_name)



for item in test:
    if item.endswith(".so"):
        print(f"[{i}] Deleting{os.path.join(dir_name, item)}")
        try:
            os.remove(os.path.join(dir_name, item))
        except:
            print(f"[!] Failed to delete {os.path.join(dir_name, item)}")
        i = i+1
        

for item in test:
    if item.endswith(".dll"):
        print(f"[{i}] Deleting {os.path.join(dir_name, item)}")
        try:
            os.remove(os.path.join(dir_name, item))
        except:
            print(f"[!] Failed to delete {os.path.join(dir_name, item)}")
        i = i+1

cython = "*.py"

print("Going to compile:")

for item in test:
    if item.endswith(".py"):
        print(f"{os.path.join(dir_name, item)}")

print("../lemon/lemon.py")

done = threading.Event()
spinner = threading.Thread(target=spin,
                            args=('Compiling! This may take a couple of minutes.', done))
spinner.start()  

with HiddenPrints():
    setup(
        ext_modules=cythonize(cython),
        script_args = ['build_ext',"--inplace"],
        
    )


test = os.listdir(dir_name)


for item in test:
    if item.endswith(".c"):
        print(f"[{i}] Deleting {os.path.join(dir_name, item)}")
        try:
            os.remove(os.path.join(dir_name, item))
        except:
            print(f"[!] Failed to delete {os.path.join(dir_name, item)}")
        i = i+1






try:
    shutil.rmtree("build")
except OSError as e:
    print("[!] Failed to delete build directory")
try:
    shutil.rmtree("__pycache__")
except OSError as e:
    print("[!] Failed to delete __pycache__ directory")

os.chdir("../lemon/")



i = 0
dir_name = "."
test = os.listdir(dir_name)
for item in test:
    if item.endswith(".so"):
        print(f"[{i}] Deleting {os.path.join(dir_name, item)}")
        try:
            os.remove(os.path.join(dir_name, item))
        except:
            print(f"[!] Failed to delete {os.path.join(dir_name, item)}")
        i = i+1
for item in test:
    if item.endswith(".dll"):
        print(f"[{i}] Deleting {os.path.join(dir_name, item)}")
        try:
            os.remove(os.path.join(dir_name, item))
        except:
            print(f"[!] Failed to delete {os.path.join(dir_name, item)}")
        i = i+1


with HiddenPrints():
    setup(
        ext_modules=cythonize("lemon.py"),
        script_args = ['build_ext',"--inplace"],
        
)
done.set() 
spinner.join()  

test = os.listdir(dir_name)

for item in test:
    if item.endswith(".c"):
        print(f"[{i}] Deleting{os.path.join(dir_name, item)}")
        try:
            os.remove(os.path.join(dir_name, item))
        except:
            print(f"[!] Failed to delete {os.path.join(dir_name, item)}")
        i = i+1


try:
    shutil.rmtree("build")
except OSError as e:
    print("[!] Failed to delete build directory")
try:
    shutil.rmtree("__pycache__")
except OSError as e:
    print("[!] Failed to delete __pycache__ directory")