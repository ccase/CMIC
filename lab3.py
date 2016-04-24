# Created by: Kevin Nguyen
# Class: Special Topics in CS
# Lab 3

import operator, sys, json, hashlib, os, struct
from heapq import merge
from math import exp

def calculateHistogram(nameOfFile):
	histogram = {}
	f = open(nameOfFile, "rb")
	while True:
		char = f.read(1)
		if not char:
			break
		if char not in histogram:
			histogram[char] = 1
		else:
			histogram[char] += 1
	f.close()
	return histogram

"""
The histogram should be an array of tuples where the tuples contain (key, value)
"""
def formatHist(hist):
	formattedHist = []
	for key,value in hist.items():
		formattedHist.append((key,value))
	return formattedHist

"""
Huff compression assigns a binary code to each key/char
"""
def huffCompress(hist):
	lst = sorted(hist, key = lambda y: y[1])
	while len(lst) > 1:
		fst = lst[0]
		snd = lst[1]
		val = fst[1] + snd[1]
		key = [fst[0], snd[0]]
		lst = lst[2:]
		lst.append([key,val])
		lst = sorted(lst, key = lambda y: y[1])
	tree = lst[0][0]
	code = []
	huffCodeGenerator(tree, "", code)
	dictCode = dict(code)
	return dictCode

def huffCodeGenerator(lst, side, code):
	if len(lst) == 1:
		code.append((lst, side))
	else:
		left = huffCodeGenerator(lst[0], side + "0", code)
		right = huffCodeGenerator(lst[1], side + "1", code)

"""
the keys should be the char order value not the actual char itself
"""
def formatCodeDict(codeDict):
	printableHist = {}
	for key,value in codeDict.items():
		printableHist[ord(key)] = value
	return printableHist

""" 
Given any input, outputs the JSON equivalent
"""
def JSONFormatter(input):
	return json.dumps(input)

"""
Given a textfile and the dictionary of char to binary value, 
convert it into a sequence of binary bits
"""
def textFileToBinary(nameOfFile, printableHist):
	encodedFile = ""
	f = open(nameOfFile, "rb")
	while True:
		char = f.read(1)
		if not char:
			break
		charVal = ord(char)
		encodedFile += printableHist[charVal]
	f.close()
	isMultipleOfEight = 8 - (len(encodedFile) % 8)
	if isMultipleOfEight != 8:
		for i in range(isMultipleOfEight):
			encodedFile += "0"
	return encodedFile

"""
Given an 8 bit binary string, generate the integer equivalent
"""
def binStringToInt(binString):
	reversedString = binString[::-1]
	val = 0
	for i in range(len(reversedString)):
		val += (int(reversedString[i]) * pow(2, i))
	return val

"""
Create a header for the compressed file
"""
def writeToNewFile(nameOfFile, JSONHist, encodedFile):
	origFile = open(nameOfFile, "rb")
	fileText = origFile.read()

	# MD5 check sum
	m = hashlib.md5()
	m.update(str(fileText))

	# Create the hash
	fileDict = {}
	fileDict["size"] = os.path.getsize(nameOfFile)
	fileDict["hash"] = m.hexdigest()
	JSONFileDict = JSONFormatter(fileDict)

	# Write everything to new file
	fileName = str(nameOfFile)+ "_encodedFile"
	f = open(fileName, "wb")
	f.write(JSONFileDict + "\n")
	f.write(JSONHist + "\n")

	for i in range(0,len(encodedFile), 8):
		f.write(struct.pack("B",binStringToInt(encodedFile[i:i+8])))
	f.close()
	origFile.close()
	return


def main():
    nameOfFile = sys.argv[1]
    try:
    	hist = calculateHistogram(nameOfFile)
    	formattedHist = formatHist(hist)
        codeDict = huffCompress(formattedHist)
        printableHist = formatCodeDict(codeDict)
        JSONHist = JSONFormatter(printableHist)
        sys.stdout.write(JSONHist + "\n")
     	encodedFile = textFileToBinary(nameOfFile, printableHist)
     	writeToNewFile(nameOfFile, JSONHist, encodedFile)
        return
    except IOError:
        print "\nError. Quitting..."
        return

# Allows the program to immediately be run when compiled.
if __name__ == "__main__":
    main()