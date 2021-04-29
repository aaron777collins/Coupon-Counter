
#test

import os
import subprocess
import ensurepip
from sys import platform
import sys

def install(package):
		subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def installAll():

	#ensuring pip is installed

	if platform == "linux" or platform == "linux2":
		subprocess.check_call(["sudo", "apt-get", "install", "python3-pip"])
	else:
		ensurepip.bootstrap()

	install("pynput")

	print("\n\n########################################\nAll Dependencies Installed.\n")
