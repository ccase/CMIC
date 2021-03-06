#CMiC Image Compressor Starter file
#first some imports
import sys
import scipy
import scipy.ndimage
import numpy as np
import PIL
import pywt
import argparse
import lab3
#wrapper for showing np.array() as an image
def show(image):
	scipy.misc.toimage(image).show()

#open the image and take the 2D DWT
#After that, it's up to you!
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input_image")
	parser.add_argument("output_file")
	parser.add_argument("--wavelet", help="wavelet name to use. Default=haar", default="db4")
	parser.add_argument("--quantize", help="quantization level to use. Default=4", type=int, default=4)
	parser.add_argument("--lq", help="quantization level to use on LL. Default=2", type=int, default=2)
	args = parser.parse_args()

	input_file_name = args.input_image
	try:
		im = scipy.ndimage.imread(input_file_name, flatten=True, mode="L")
		print "Attempting to open %s..." % input_file_name
	except:
		print "Unable to open input image. Qutting."
		quit()
	#show(im)
	#get height and width
	(height, width) = im.shape
	wavelet = args.wavelet
	q = args.quantize
	lq = args.lq
	
	'''Account for odd'''
	newHeight = height
	if height%2 != 0:
		z = np.zeros((1,width),dtype=float)
		im = np.append(im, z, axis=0)
		newHeight = height+1
	if width%2 != 0:
		z = np.zeros((newHeight, 1), dtype = float)
		im = np.append(im, z, axis=1)

	print im.shape
	LL, (LH, HL, HH) = pywt.dwt2(im, wavelet, mode='periodization')

	'''Quantize then differential encoding'''
	flatLL = (LL/lq).flatten()
	flatLL = np.insert(flatLL, 0, 0)
	LLdiff = np.diff(flatLL.astype(int))
	LLlist = list(LLdiff)


	'''Quantization'''
	LHq = LH / q
	HHq = HH / q
	HLq = HL / q

	LHint = LHq.flatten().astype(int)
	HHint = HHq.flatten().astype(int)
	HLint = HLq.flatten().astype(int)

	LHlist = list(LHint)
	HHlist = list(HHint)
	HLlist = list(HLint)




	'''Huffman pre'''
	fullList = LLlist + LHlist + HLlist + HHlist
	headerMap = {}
	headerMap["height"] = height
	headerMap["width"] = width
	headerMap["wavelet"] = wavelet
	headerMap["q"] = q
	headerMap["lq"] = lq
	print headerMap
	lab3.fullHuffman(fullList, headerMap, args.output_file)



	
	'''the following block of code will let you look at the decomposed image. Uncomment it if you'd like
	
	dwt = np.zeros((newHeight, width))
	dwt[0:newHeight/2, 0:width/2] = LL
	dwt[newHeight/2:,0:width/2] = HL
	dwt[0:newHeight/2, width/2:] = LH
	dwt[newHeight/2:,width/2:] = HH
	show(dwt)
	'''

if __name__ == '__main__':
	main()