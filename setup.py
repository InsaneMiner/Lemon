import sys 
import zipfile 
import os
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file) , os.path.relpath(os.path.join(root, file), path) )
  




if len(sys.argv) < 2:
    
	import re

	from setuptools import setup, find_packages

	setup(
		name="lemon",
		version='1.2.1',
		author='Joel Schofield',
		author_email='none@none.none',
		url='https://github.com/InsaneMiner/Lemon',
		license='LICENSE',
		description='Web framework and web server written in python',
		long_description=open('README.md').read(),
		packages=["lemon","lemon.libs"],
		package_data={'': ['default.zip']},
		include_package_data=True,
		
		
	)
elif sys.argv[1] == "dev_build":
	zipf = zipfile.ZipFile('lemon/default.zip', 'w', zipfile.ZIP_DEFLATED)
	zipdir('lemon/default', zipf)
	zipf.close()

else:
	import re

	from setuptools import setup, find_packages

	setup(
		name="lemon",
		version='1.2.1',
		author='Joel Schofield',
		author_email='none@none.none',
		url='https://github.com/InsaneMiner/Lemon',
		license='LICENSE',
		description='Web framework and web server written in python',
		long_description=open('README.md').read(),
		packages=["lemon","lemon.libs"],
		package_data={'': ['default.zip']},
		include_package_data=True,
		
		
	)