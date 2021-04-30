
# Coupon reading code
# Created by Aaron Collins

import os
import subprocess
import time

import dependencies
dependencies.installAll()

#global variables
running = True
readingChars = False
cmdBuffer = ""
codes = []
codesName = "codes.txt"



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


def attemptExecution():
	global cmdBuffer

	printBuffer()


	for code in codes:
		if cmdBuffer == code:
			clearBuffer()
			changeMode() #stop reading input
			break

def on_press(key):
	global running, readingChars, cmdBuffer

	if(key == Key.backspace):
		if (cmdBuffer != None and len(cmdBuffer)!=0):
			cmdBuffer = cmdBuffer[0:-1]
			printBuffer()
	if(key == Key.esc):
		running=False
		return False

	try:
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


def init():
	global codes, codesName

	if(not os.path.exists(codesName)):
		with open(codesName, 'w') as reader:
			reader.write("samplecode1, samplecode2")

	with open(codesName, 'r') as reader:
		fileData = reader.read()
		fileList = fileData.split(",")
		for item in fileList:
			item = item.strip()
			codes.append(item)


	printCodes()

def main():

	init()

	while(running):
		time.sleep(1)
	exit()

if __name__ == "__main__":
	main()
