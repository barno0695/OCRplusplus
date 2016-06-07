author = "barno"

directory = '/var/www/html/OCR++/myproject/media/documents/'


def comma(y):
	x = y.strip()
	if x[len(x)-1] == ',':
		return "1"
	else:
		return "0"


fs = ''

inputfile = []

titlecount = 0;
authorcount = 0;
maxfs = 0
flag = "0"   # to check if a title is already going on
end = 0
with open(directory + 'final.txt','r') as f:
	for line in f:
		abc = line.split()

		if len(abc) > 1:  # if not a blank line
			if float(abc[4]) > maxfs:
				maxfs = float(abc[4])
			inputfile.append(abc)
			if abc[12] == '1':
				titlecount = titlecount + 1
			if abc[12] == '2':
				authorcount = authorcount + 1

if titlecount == 0:
	fi = open(directory + 'final.txt','w+')
	# print len(inputfile)
	fi.seek(0)
	l = ""
	for abc in inputfile:
		if float(abc[4]) == maxfs:
			# print "yo"
			l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t" + abc[11] +"\t1\n"
		else:
			l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t"+ abc[11] + "\t"+ abc[12] + "\n"
		
		fi.write(l);			

	fi.truncate()
	fi.close()