import os
import re
import csv
newref = '0\t0\t0\t0\t0\t0\t0'

import glob

directory = '/var/www/html/OCR++/myproject/media/documents/testResults/'

file_name = glob.glob(directory+'*.txt')
#print file_name

def findUrl( substring, mylist = []):
	index = -1

	url = []
	idx = -1
	i=0
	newstring = ""
	urlString = ""
	while i<len(mylist):
		x = mylist[i]
		if substring in x:
			#print x
			idx = i
			# #print "aaaaa = "
			# #print idx
			# #print mylist[idx]
			index = x.find(substring)
			#print index
			#print len(x)
			# if index!=-1:
			while((x[index]!=" " and x[index]!="\n" and x[index]!="\t") and index<=(len(x)-1)):
				url.append(x[index])
				x = x[:index] + x[index+1:]
				# #print x
				# #print len(x)
				# index++
			#print x
			newstring = x
			#print url
			urlString = "".join(url)
			#print urlString
		i+=1

	return (urlString, idx, newstring)

srno = 1
for fname in file_name:
	srno = srno+1
	fn = fname.split('/')
	fn = fn[-1]
	#print fn

	txtFilename = directory + fn[:-4] + '.txt'
	xmlFilename = directory +'xmls/'+ fn[:-4] + '.xml'

	xmlFile = open(xmlFilename,'a')
	flag = True
	reference = []
	references = [[]]

	lines = [line.rstrip('\n') for line in open(txtFilename)]

	# #print lines
	for line in lines:
		#print line
		l = line.split('\t')
		#print l
		if line==newref:
			flag = False
		if flag:
			reference.append(line)
		else:
			references.append(reference)
			flag=True
			reference = []

	# references.append(reference)
	# #print "len = " + str(len(references))
	#print references[-1]

	for ref in references:
		if len(ref)<=0 or ref=='':
			references.remove(ref)

	tag = 0

	#print "len = " + str(len(references))


	for reference in references:
		author = []
		title = []
		journal =[]
		publisher=[]
		year=[]
		url=[]
		booktitle=[]
		biblS=[]
		volume = []
		pagenumber=[]
		location=[]
		editor=[]
		if len(reference)==0:
			continue
		for row in reference:
			row = str(row)
			# #print row
			if len(row)==0:
				continue
			lastwords = row.split("\t")
			tag = lastwords[-1]
			# #print tag
			if tag==0:
				continue
			i=0
			# #print tag
			# #print
			if tag=="1":
				# #print "author"
				while(row[i]!='\t'):
					author.append(row[i])
					i+=1
				author.append(" ")
			elif tag=="2":
				# #print "title"
				while (row[i]!='\t'):
					title.append(row[i])
					i+=1
				title.append(" ")
			elif tag=="3":
				while (row[i]!='\t'):
					journal.append(row[i])
					i+=1
				journal.append(" ")
				# #print "journal = "
				# #print journal
			elif tag=="4":
				# #print "publisher"
				while (row[i]!='\t'):
					publisher.append(row[i])
					i+=1
				publisher.append(" ")
				# #print "publisher "
				# #print publisher
			elif tag=="5":
				# #print "year"
				while (row[i]!='\t'):
					year.append(row[i])
					i+=1
				year.append(" ")
			elif tag=="6":
				# #print "url"
				while (row[i]!='\t'):
					url.append(row[i])
					i+=1
				url.append(" ")
			elif tag=="7":
				# #print "booktitle"
				while (row[i]!='\t'):
					booktitle.append(row[i])
					i+=1
				booktitle.append(" ")
			elif tag=="8":
				# #print "volume"
				while (row[i]!='\t'):
					volume.append(row[i])
					i+=1
				volume.append(" ")
			elif tag=="9":
				# #print "pagenumber"
				while (row[i]!='\t'):
					pagenumber.append(row[i])
					i+=1
				pagenumber.append(" ")
			elif tag=="10":
				while (row[i]!='\t'):
					location.append(row[i])
					i+=1
				location.append(" ")
				# #print "location = "
				# #print location
			elif tag=="11":
				while (row[i]!='\t'):
					editor.append(row[i])
					i+=1
				editor.append(" ")
			# 	#print "editor "
			# 	#print editor
			# # #print row

		# urlSub = "http"
		title = "".join(title)
		author = "".join(author)
		journal = "".join(journal)
		publisher = "".join(publisher)
		year = "".join(year)
		url = "".join(url)
		volume = "".join(volume)
		booktitle = "".join(booktitle)
		pagenumber = "".join(pagenumber)
		location = "".join(location)
		editor = "".join(editor)
		# #print editor
		#print author
		#print title
		xmlFile.write("<author>"+author+"</author>" +"\n")
		xmlFile.write("<title>"+title+"</title>" +"\n")
		xmlFile.write("<journal>"+journal+"</journal>" +"\n")
		xmlFile.write("<publisher>"+publisher+"</publisher>" +"\n")
		xmlFile.write("<year>"+year+"</year>" +"\n")
		# xmlFile.write("<url>"+url+"</url>" +"\n")
		xmlFile.write("<booktitle>"+booktitle+"</booktitle>" +"\n")
		xmlFile.write("<volume>"+volume+"</volume>" +"\n")
		xmlFile.write("<pagenumber>"+pagenumber+"</pagenumber>" +"\n")
		xmlFile.write("<location>"+location+"</location>" +"\n")
		xmlFile.write("<editor>"+editor+"</editor>" +"\n")
		xmlFile.write("\n")
		# #print title
		# #print



	# with open(fname) as f:
	#     content = f.readlines()
	#     #print content
