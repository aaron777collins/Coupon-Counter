
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

def attemptExecution():
	global cmdBuffer

	print("Current input: " + cmdBuffer)

	if cmdBuffer == "m10":
		clearBuffer()
		changeMode() #stop reading input

def on_press(key):
	pass

def on_release(key):

	global running, readingChars

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

listener = Listener( on_press=on_press, on_release=on_release)

listener.start()


def main():
	while(running):
		time.sleep(1)
	exit()

if __name__ == "__main__":
	main()
