#cython: language_level=3
import os
import config.config

def move_uploaded_file(tempfile,newfile):
	try:
		with open(f"{config.config.TEMP}/{tempfile}","r") as f:
			pass
	except:
		return "File does not exist"

	try:
		os.rename(f"{config.config.TEMP}/{tempfile}", newfile)
	except:
		return "Failed"

