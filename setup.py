import sys 
import zipfile 
import os
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file) , os.path.relpath(os.path.join(root, file), path) )
  

name, version = ("lemon-framework", "1.2.2")


if len(sys.argv) < 2 and sys.argv[1] == "dev_build":
	zipf = zipfile.ZipFile('lemon/default.zip', 'w', zipfile.ZIP_DEFLATED)
	zipdir('lemon/default', zipf)
	zipf.close()

else:
	import re

	from setuptools import setup, find_packages

	setup(
		name=name,
		version=version,
		author='Joel Schofield',
		author_email='none@none.none',
		url='https://github.com/InsaneMiner/Lemon',
		license='LICENSE',
		description='Web framework and web server written in python',
		long_description=open('README.md').read(),
		packages=["lemon","lemon.libs"],
		package_data={'': ['default.zip']},
		include_package_data=True,
		install_requires = ["urllib2","regex","asyncio","watchdog","shutil"],
	)
