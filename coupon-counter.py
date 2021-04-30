
# Coupon reading code
# Created by Aaron Collins

import os
import subprocess
import time
import csv
from datetime import datetime
import atexit
import signal

import dependencies
dependencies.installAll()

import tkinter as tk
from tkinter import simpledialog


#global variables
running = True
readingChars = False
cmdBuffer = ""
codes = []
codesName = "codes.txt"
csvFileName = "codesData.csv"
csvFile = None
csvWriter = None
locationFileName = "location.txt"
location = ""

from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()

def removeChar():
	keyboard.press(Key.backspace)
	keyboard.release(Key.backspace)

def clearBuffer():
	global cmdBuffer

	if (cmdBuffer == None):
		return

	for i in range(len(cmdBuffer)):
		removeChar()
	cmdBuffer = ""


def changeMode():
	global readingChars, cmdBuffer
	readingChars = not readingChars
	cmdBuffer = ""



def addToBuffer(key):
	global cmdBuffer
	if(cmdBuffer != None):
		cmdBuffer = cmdBuffer + str(key.char)
	else:
		cmdBuffer = "" + str(key.char)

def printBuffer():
	global cmdBuffer
	print("Current input: " + cmdBuffer)

def askLocation():
	root = tk.Tk()

	root.withdraw()

	locationResult = ""

	while(locationResult == ""):

		#ask for input
		userInput = simpledialog.askstring(title="Location?", prompt="What location is this for?\nd - Devonshire\nt - Tecumseh")

		if(userInput.upper() == "D"):
			locationResult = "DEVONSHIRE"

		if(userInput.upper() == "T"):
			locationResult = "TECUMSEH"

	root.destroy()

	return locationResult

def attemptExecution():
	global cmdBuffer, csvWriter, location

	printBuffer()


	for code in codes:
		if cmdBuffer.upper() == code.upper():
			clearBuffer()
			changeMode() #stop reading input

			locationChoice = location

			#check if we need to ask for the location
			if(location == 'CHOOSE'):
				#we need to ask the location
				locationChoice = askLocation()

			#write to csv file
			csvWriter.writerow([locationChoice, datetime.now().strftime("%Y/%m/%d"), code])

			break

def on_press(key):
	global running, readingChars, cmdBuffer

	if(key == Key.backspace):
		if (cmdBuffer != None and len(cmdBuffer)!=0):
			cmdBuffer = cmdBuffer[0:-1]
			printBuffer()

	try:
		if(key.char == '\\'):
			running=False
			removeChar()
			return False

		if(key.char == '`'):
			removeChar()
			changeMode()
		else:
			if readingChars:
				addToBuffer(key)
				attemptExecution()


	except AttributeError:
		pass





def on_release(key):
	pass

listener = Listener( on_press=on_press, on_release=on_release)

listener.start()


def printCodes():
	global codes

	print("The following codes were detected:")
	for code in codes:
		print(code)

def askLocationWithChooseOption():
	root = tk.Tk()

	root.withdraw()

	locationResult = ""

	while(locationResult == ""):

		#ask for input
		userInput = simpledialog.askstring(title="Location?", prompt="What location is this for?\nd - Devonshire\nt - Tecumseh\nc - Choose every time")

		if(userInput.upper() == "D"):
			locationResult = "DEVONSHIRE"

		if(userInput.upper() == "T"):
			locationResult = "TECUMSEH"

		if(userInput.upper() == "C"):
			locationResult = "CHOOSE"

	root.destroy()

	return locationResult


def init():
	global codes, codesName, csvFileName, csvFile, csvWriter, locationFileName, location

	#seeing if location file exists
	if(not os.path.exists(locationFileName)):
		with open(locationFileName, 'w') as writer:
			#asking user for location and writing their choice
			location = askLocationWithChooseOption()
			print("Chosen location: " + location)
			writer.write(location)
	else:
		with open(locationFileName, 'r') as reader:
			location = reader.read().strip()

	#creating base csv file if it doesn't exist
	if(not os.path.exists(csvFileName)):
		with open(csvFileName, 'w', newline='\n') as tempCsvFile:
			tempCsvWriter = csv.writer(tempCsvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			tempCsvWriter.writerow(['Location', 'Time', 'Code'])

	csvFile = open(csvFileName, 'a', newline='\n') #open csv file for appending
	csvWriter = csv.writer(csvFile, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)

	#Creating sample code file if the code file doesn't exist
	if(not os.path.exists(codesName)):
		with open(codesName, 'w') as reader:
			reader.write("samplecode1, samplecode2")

	#reading from code file
	with open(codesName, 'r') as reader:
		fileData = reader.read()
		fileList = fileData.split(",")
		for item in fileList:
			item = item.strip()
			codes.append(item)


	printCodes()
	print("Press \ to save the results and exit")

	#ensures files are saved at exit
	atexit.register(exitSafely)

	signal.signal(signal.SIGTERM, exitSafely)


def exitSafely():
	global csvFile
	csvFile.close()
	print("Saved CSV File before exiting...")
	exit()

def main():

	global csvFile

	init()

	while(running):
		time.sleep(1)

	#close csv file (save changes)
	csvFile.close()

	exit()

if __name__ == "__main__":
	main()
