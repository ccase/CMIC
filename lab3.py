# Created by: Kevin Nguyen
# Class: Special Topics in CS
# Lab 3

import operator, sys, json, hashlib, os, struct
from heapq import merge
from math import exp

def calculateHistogram(lst):
	histogram = {}
	i = 0
	while i < len(lst):
		# keys must be a string
		char = str(lst[i])
		if char not in histogram:
			histogram[char] = 1
		else:
			histogram[char] += 1
		i += 1
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

def huffCodeGenerator(inputList, side, code):
	# could've been a numpy.float32 so if it's anything but a list then it's over
	if not isinstance(inputList, list):
		code.append((inputList, side))
	else:
		left = huffCodeGenerator(inputList[0], side + "0", code)
		right = huffCodeGenerator(inputList[1], side + "1", code)

"""
the keys should be the char order value not the actual char itself
"""
def formatCodeDict(codeDict):
	printableHist = {}
	for key,value in codeDict.items():
		printableHist[key] = value
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
def textFileToBinary(lst, printableHist):
	encodedFile = ""
	i = 0
	while i < len(lst):
		# keys must be a string
		char = str(lst[i])
		if not char:
			break
		charVal = char
		encodedFile += printableHist[charVal]
		i += 1
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
def writeToNewFile(out, headerMap, JSONHist, encodedFile):

	# Write everything to new file
	f = open(out, "wb")
	f.write(headerMap + "\n")
	f.write(JSONHist + "\n")

	for i in range(0,len(encodedFile), 8):
		f.write(struct.pack("B",binStringToInt(encodedFile[i:i+8])))
	f.close()
	return


def fullHuffman(lst, headerMap, out):
    try:
    	hist = calculateHistogram(lst)
    	formattedHist = formatHist(hist)
        codeDict = huffCompress(formattedHist)
        printableHist = formatCodeDict(codeDict)
        JSONHist = JSONFormatter(printableHist)
        JSONHeaderMap = JSONFormatter(headerMap)
        #sys.stdout.write(JSONHist + "\n")
     	encodedFile = textFileToBinary(lst, printableHist)
     	writeToNewFile(out, JSONHeaderMap, JSONHist, encodedFile)
        return codeDict
    except IOError:
        print "\nError. Quitting..."
        return

def decode(input_file_name, output_file_name, code_dict):
	#quantization factor. Might change
	input_file = open(input_file_name, 'rb')
	decode_dict = {v.encode() : k for k, v in code_dict.iteritems()}
	#print decode_dict

	binary_data = input_file.read()
	binary_string = ""
	
	for byte in binary_data:
		binary_string += format(ord(byte),'08b')
	
	decdoed_data = []
	
	while len(decdoed_data) != 8:
		sub_str = ""
		i = 0
		while sub_str not in decode_dict:
			sub_str = binary_string[0:i]
			i=i+1
		decdoed_data += [int(decode_dict[sub_str])]
		binary_string = binary_string[i-1:]

	
	print decdoed_data

if __name__ == '__main__':
	codeDict = fullHuffman([1,1,1,1,2,2,3,1], "t", "test.txt")
	decode("test.txt", "testDecoded.txt", codeDict)



