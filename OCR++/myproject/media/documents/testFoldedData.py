import os
import glob
import subprocess
from subprocess import Popen, PIPE
import unicodedata

directory = '/var/www/html/OCR++/myproject/media/documents/'

file_name = glob.glob(directory+'test_files/*.txt')
# #print file_name

srno = 1
# for ff in

for fname in file_name:
	srno = srno+1
	fn = fname.split('/')
	fn = fn[-1]
	# #print fname
	#print fn

	model = directory + "ref_model_file.txt"
	# print "modelFile = " + model
	# subprocess.call("mkdir " + directory + "testResults", shell=True)
	# subprocess.call("mkdir " + directory + "testResults/xmls", shell=True)
	#
	# subprocess.call("mkdir " + directory + "testFiles", shell=True)
	test_file = directory + "test_files/"+fn
	test_fileR = directory + "testResults/"+fn
	# #print
	# #print template
	# #print fname
	# string = "crf_learn "+ template +" "+ train_file + " "+ modelFile
	# #print string
	subprocess.call("crf_test -m "+ model +" "+ test_file + " >> "+ test_fileR, shell=True)
	# # #print lines
# #print srno
