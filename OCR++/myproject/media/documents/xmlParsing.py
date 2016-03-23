__author__ = 'ManviG'

import xml.etree.ElementTree as ET
import re
import os
import string
import sys
import types
import glob

# tree = ET.parse('/home/manvi/Documents/acads/NLP/pdfs/Springer1.xml')
# root = tree.getroot()


import unicodedata

months = ["January", "February", "March", "April", "May", "June", "July","August", "September", "October"
			"November","December","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

country_list = ["America", "UK", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla",
				"Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas",
				"Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda",
				"Bhutan", "Bolivia", "Herzegowina", "Botswana", "Island","Brazil", "Brunei", "Bulgaria",
				"Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad",
				"Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Ivoire", "Croatia", "Cuba",
				"Cyprus", "Denmark", "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea",
				"Estonia", "Ethiopia", "Fiji", "Finland", "France","Territories",
				"Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada",
				"Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras",
				"Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
				"Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait",
				"Kyrgyzstan", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
				"Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
				"Malta", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova",
				"Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
				"Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria",
				"Niue", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Paraguay", "Peru", "Philippines",
				"Pitcairn", "Poland", "Portugal", "Rico", "Qatar", "Romania", "Russia", "Federation", "Rwanda",
				"Samoa", "Arabia", "Senegal", "Seychelles", "Singapore", "Slovakia", "Slovenia",
				"Somalia", "South Africa", "Spain", "Lanka", "Helena", "Miquelon", "Sudan", "Suriname",
				"Swaziland", "Sweden", "Switzerland", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo",
				"Tokelau", "Tonga", "Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
				"Emirates", "Kingdom", "States", "Uruguay", "USA", "UAE", "Uzbekistan", "Vanuatu", "Venezuela",
				"Vietnam", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

US_States = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
			"Connecticut", "Delaware", "Columbia", "Florida", "Georgia", "Hawaii", "Idaho",
			"Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
			"Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
			"Nevada", "Hampshire", "Jersey", "York", "Carolina", "Dakota", "Ohio", "Oklahoma", "Oregon",
			"Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin",
			"Wyoming"]



def caps(y):
	x=y.strip()
	if x.islower():
		return "0"
	elif x.isupper():
		return "1"
	elif x.isdigit():
		return "2"
	elif x[:-1].isdigit():
		return "3"
	elif x[1:].islower() and x[0].isupper():
		return "4"
	elif y.isupper():
		return "6"
	elif y.islower():
		return "7"
	else:
		return "5"

regYearFound = False
regPageFound = False
regVolFound = False

def yearPageUrl(y):
	regYear = re.compile('^\(?\d{4}[a-z]?\)?')
	regPage = re.compile('\d{1,4}\-\d{1,4}|\d{5,8}')
	regVol = re.compile('^\d{1,3}\(\d+\)')
	regURL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[\$-_@.&+]|[!*\(\),]|(?:\%[0-9a-fA-F][0-9a-fA-F]))')
	regYearFound = bool(re.search(regYear,y))
	regPageFound = bool(re.search(regPage,y))
	regVolFound = bool(re.search(regVol,y))
	regURLFound = bool(re.search(regURL,y))
	if regYearFound:
		regYearFound = False
		regVolFound = False
		regPageFound = False
		regURLFound = False
		return "1"
	elif regURLFound:
		regYearFound = False
		regVolFound = False
		regPageFound = False
		regURLFound = False
		return "4"
	elif regVolFound:
		regYearFound = False
		regVolFound = False
		regPageFound = False
		regURLFound = False
		return "2"
	elif regPageFound:
		regYearFound = False
		regVolFound = False
		regPageFound = False
		regURLFound = False
		return "3"
	else:
		return "0"


def whichWord(y):
	x = y.strip()
	# #print z
	# z = z.lower()
	regPage = re.compile("[pP]age|pp")
	regVol = re.compile("[vV]ol|[vV]olume|[vV]ol")
	regEd = re.compile("[eE]ds|[eE]ditor")
	regJournal = re.compile("[Jj]ournal")
	regPub1 = re.compile("[pP]ress")
	regPub2 = re.compile("[pP]ublication")
	regPub3 = re.compile("[pP]ublish")
	regBt = re.compile("[cC]onference|[Pp]roceeding")

	colon_index = x.find(":")
	dot_index = x.find(".")
	comma_index = x.find(",")
	#print x
	if colon_index==len(x)-1 or dot_index==len(x)-1 or comma_index==len(x)-1:
		z= x[:-1]
	else:
		z = x
		# #print z
	#print z

	if bool(re.search(regJournal,x)):
		#print x
		#print re.findall(regJournal,x)
		return "4"
	elif bool(re.search(regPage,x)):
		return "1"
	elif bool(re.search(regVol,x)) or x=="no.":
		return "2"
	elif  bool(re.search(regPub1,x)) or bool(re.search(regPub2,x)) or bool(re.search(regPub3,x)):
		return "3"
	elif bool(re.search(regEd,x)):
		return "5"
	elif z in months:
		return "6"
	elif bool(re.search(regBt,x)) or x=="Proc":
		return "7"
	elif z in country_list or z in US_States:
		return "8"
	elif x=="In":
		return "9"
	else:
		return "0"

def binary(x):
    if x == "yes":
        return "1"
    return "0"


def spclChar(y):
	if '?' in y or '!' in y:
		# #print y
		return "3"
	elif ':' in y:
		# #print y
		return "1"
	elif '\"' in y:
		#print y
		return "2"
	elif '\'' in y:
		#print y
		return "4"
	elif '>' in y or '<' in y:
		return "5"
	elif '@' in y:
		return "6"
	elif '/' in y:
		return "7"
	else:
		return "0"

directory = '/var/www/html/OCR++/myproject/media/documents/'


file_name = glob.glob(directory+'input.xml')
#print file_name
#print

srno = 1
for fname in file_name:
	srno = srno+1
	fn = fname.split('/')
	fn = fn[-1]
	#print fn
	#print

	xmlFile =directory + fn[:-4] + '.xml'
	txtFile =directory+ 'test_files/' + fn[:-4] + '.txt'
	f = open(txtFile, 'a')
	tree = ET.parse(xmlFile)
	root = tree.getroot()

	max_fs = 0
	for pages in root.findall('PAGE'):
	    for texts in pages.findall('TEXT'):
	        for token in texts.findall('TOKEN'):
	            if(float(token.attrib['font-size'])>max_fs):
	                max_fs=float(token.attrib['font-size'])

	flag = False
	reg_ex = True

	Reference = []

	for pages in root.findall('PAGE'):
	    texts = pages.findall('TEXT')
	    for i  in range(len(texts)):

	        tokens = texts[i].findall('TOKEN')

	    	if flag==False:

	        	for j in range(len(tokens)):
					if type(tokens[j].text) is unicode:
						word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
	            	else:
	            		word = tokens[j].text
	            		if isinstance(word, types.NoneType):
	            			#print " word type is NoneType"
	            			continue
	            	if(len(word.replace(' ',''))>0):
	            	    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
	            	        #print word + " now that's it"
	            	        flag = True
	            	        first_text = True
	            	        continue
	        else:
				cur_x = texts[i].attrib['x']
				cur_y = texts[i].attrib['y']
				cur_size = float(tokens[0].attrib['font-size'])
				cur_font = tokens[0].attrib['font-name']
				cur_font = cur_font.lower()
				cur_bold = tokens[0].attrib['bold']
				cur_italic = tokens[0].attrib['italic']
				if first_text:
					start_ref = cur_x
					idx = 0
					Reference.append(" ")
					first_height = float(texts[i+1].attrib['y']) - float(cur_y)
					first_size = float(tokens[0].attrib['font-size'])
					first_font = tokens[0].attrib['font-name'].lower()
					first_lower = first_font.lower()
					first_bold = tokens[0].attrib['bold']
					first_italic = tokens[0].attrib['italic']
					first_text = False


				else:
					if (float(cur_y) < float(prev_y)):
						if cur_size < first_size - 0.1 or cur_size > first_size + 0.1 or cur_font != first_font or cur_bold != first_bold or cur_italic != first_italic:
							##print str(cur_size) + " " + cur_font + " " + cur_bold + " " + cur_italic
							##print str(first_size) + " " + first_font + " " + first_bold + " " + first_italic
							# #print "a"
							continue
						k = i + 1
						while(True):
							if k >= len(texts):
								start_ref = cur_x
								break
							next_x = texts[k].attrib['x']
							if(float(next_x) > float(cur_x) + 0.1):
								start_ref = cur_x
								idx = idx + 1
								f.write("0\t0\t0\t0\t0\t0\n\n")
								Reference.append(" ")
								break
							if(float(next_x) < float(cur_x) - 0.1):
								start_ref = next_x
								break
							k = k + 1
					else:
						if float(cur_y) - float(prev_y) > 3 * first_height:
							# #print "b"
							continue

						if (float(cur_x) < float(start_ref) + 0.1 ):
							idx = idx + 1
							f.write("0\t0\t0\t0\t0\t0\n\n")
							Reference.append(" ")

				prev_x = cur_x
				prev_y = cur_y


				for j in range(len(tokens)):
					if type(tokens[j].text) is unicode:
						word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
					else:
						word = tokens[j].text
						if isinstance(word, types.NoneType):
							#print " word type is NoneType"
							continue
					if(len(word.replace(' ',''))>0):
						Reference[idx] += word
						Reference[idx] += " "
						#print whichWord(word.encode("utf-8"))
						f.write((word.replace(' ','')+"\t").encode("utf-8"))
						# f.write(((binary(tokens[j].attrib['italic'])).replace(' ','')+"\t").encode("utf-8"))
						f.write((spclChar(word.encode("utf-8").replace(' ','')))+"\t")

						f.write((caps(word.encode("utf-8").replace(' ','')))+"\t")
						f.write((whichWord(word.encode("utf-8").replace(' ','')))+"\t")
						f.write((yearPageUrl(word.encode("utf-8").replace(' ','')))+"\t\n")
				f.write("0\t0\t0\t0\t0\t0\n\n")

	# for refs in Reference:
	# 	#print refs
	# 	#print
	# 	#print
