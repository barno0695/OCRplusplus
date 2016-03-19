author = "barno"

import xml.etree.ElementTree as ET

directory = 'myproject/media/documents/'

# directory = './'

tree = ET.parse(directory + 'input.xml')
root = tree.getroot()

l = 0

import os.path
if os.path.exists(directory + 'eval_Secmap.txt'):
	with open(directory + 'eval_Secmap.txt','r') as f:
		for line in f:
			l = l + 1
# print l
first_chunk = ""

if l > 1:

	sectree = ET.parse(directory + 'Secmap.xml')
	secroot = sectree.getroot()

	flag = 0

	# first_chunk = ""
	# print "yo"
	# for secmap in secroot.findall('sec_map'):
	#	 print "yo"
	for secs in secroot.findall('section'):
		# print "yo"
		for chunk in secs.findall('chunk'):
			# print "yo"
			first_chunk = chunk.text.replace(' ','')
			# print first_chunk
			break
		break
		# break

# print "f " + first_chunk
import unicodedata

def binary(x):
	if x == "yes":
		return "1"
	return "0"

def startCaps(y):
	x=y.strip()
	if x[0].isupper():
		return "1"
	else:
		return "0"
def comma(y):
	x = y.strip()
	if x[len(x)-1] == ',':
		return "1"
	else:
		return "0"

def commonwords(y):
	x = y.strip()
	if x == "The" or x == "and" or x == "of" or x == "Student" or x == "Senior" or x == "Junior" or x == "Member":
		return "1"
	else:
		return "0"

# def comma(y):
#	 x = y.strip()
#	 if x[len(x)-1] == ',':
#		 return "1"
#	 else:
#		 return "0"

temp = first_chunk

# print "titleauthorparse starting"
#To find max font size and total number to textxs in the file
page = 0
max_fs = 0
tot_txt_chunk = 0
tot_txt = 0
chunk_over = 0
for pages in root.findall('PAGE'):
	page = page + 1
	for texts in pages.findall('TEXT'):
		if chunk_over == 0:
			tot_txt_chunk = tot_txt_chunk + 1
		tot_txt = tot_txt + 1
		for token in texts.findall('TOKEN'):
			if token.text is None:
				continue

			word = token.text

			word = word.replace(' ','')

			# print word
			if word == first_chunk[:len(word)]:
				first_chunk = first_chunk[len(word):]
			if len(first_chunk) == 0:
				chunk_over = 1
			

			if(float(token.attrib['font-size'])>max_fs):
				# print token.text
				# if chunk_over == 0:
				max_fs=float(token.attrib['font-size'])
		
	#	 if chunk_over == 1:
	#		 break
	# if chunk_over == 1:
	#	 break


f = open(directory + 'test.txt','w')
# f.write("0\t0\t0\t0\t0\t0\n")

first_chunk = temp

# print first_chunk

# print "***"
# print tot_txt
flagg=0
txt = 0;
count = 0;
chunk_over = 0;
for pages in root.findall('PAGE'):
	count = count +1
	if count > 2:	 #Only first two pages to search
		break
	for texts in pages.findall('TEXT'):


		txt = txt + 1;
		for token in texts.findall('TOKEN'):
			if token.text is None:
				continue

			# if type(token.text) is unicode:
			# 	word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
			# else:
			word = token.text

			word = word.replace(' ','')

			# print word
			# print len(first_chunk)
			if word == first_chunk[:len(word)]:
				first_chunk = first_chunk[len(word):]
			if len(first_chunk) == 0:
				chunk_over = 1

			if(len(word)>0):
				f.write((word+"\t").encode("utf-8"))
				f.write((binary(token.attrib['bold'])+"\t").encode("utf-8")) #Bold
				f.write((str(round(float(txt)/(tot_txt),2))+"\t").encode("utf-8")) #Relative position overall
				if float(txt) > tot_txt_chunk:
					f.write("0\t")
				else:
					f.write((str(round(float(txt)/(tot_txt_chunk),2))+"\t").encode("utf-8")) #Relative position in chunk
				if max_fs != 0:
					f.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8")) #Relative size
				else:
					f.write("00\t")
				f.write((startCaps(token.text.encode("utf-8").replace(' ','')))+"\t") #Starts with caps
				f.write((comma(token.text.encode("utf-8").replace(' ','')))+"\t") #Contains comma
				f.write((commonwords(token.text.encode("utf-8").replace(' ','')))+"\t") #Common word
				f.write((str(token.attrib['y'])+"\t").encode("utf-8")) #Y-coordinate
				f.write((str(token.attrib['x'])+"\t").encode("utf-8")) #X-coordinate
				f.write((str(token.attrib['width'])+"\t").encode("utf-8")) #width
				f.write(("0\n").encode("utf-8"))


		f.write("00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\n")
		if chunk_over == 1 and l > 1:
			break
	if chunk_over == 1 and l > 1:
		break

		# f.write("0\t0\t0\t0\t0\t0\n\n")

f.write("00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00")

f.close()

# relpos = 0
# lines = []
# with open(directory + 'test.txt','r') as ft:
# 	for line in ft:
# 		# print line
# 		abc = line.split()
# 		if len(abc) > 1:  # if not a blank line
# 			# print line
# 			if float(abc[2]) != relpos:
# 				lines.append("00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00")
# 			lines.append(line)
# 			relpos = abc[2]

# print lines

# f = open(directory + 'test.txt','w')
# for line in lines:
# 	f.write(line + "\n")
# f.close()
# print "titleauthorparse Done"