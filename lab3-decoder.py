# Created by: Kevin Nguyen
# Class: Special Topics in CS
# Lab 3 Part C

import json, hashlib, sys

def decompressFile(nameOfFile):
	inputFile = open(nameOfFile, "rb")
	header = json.loads(inputFile.readline())
	huffmanCodes = json.loads(inputFile.readline())
	huffMap = {val:key for key, val in huffmanCodes.iteritems()}

	binData = inputFile.read()
	binDataStr = ""

	for byte in binData:
		binDataStr += format(ord(byte), "08b")

	decodedData = ""
	while len(decodedData) < header["size"]:
		code = ""
		i = 1
		while code not in huffMap:
			code = binDataStr[0:i]
			i += 1
		decodedData += chr(int(huffMap[code]))
		binDataStr = binDataStr[i-1:]

	if hashlib.md5(decodedData).hexdigest() == header["hash"]:
		resultFile = nameOfFile + "_decodedFile"
		outputFile = open(resultFile, "wb")
		outputFile.write(decodedData)
		outputFile.close()

def main():
    nameOfFile = sys.argv[1]
    try:
    	decompressFile(nameOfFile)
        return
    except IOError:
        print "\nError. Quitting..."
        return

# Allows the program to immediately be run when compiled.
if __name__ == "__main__":
    main()