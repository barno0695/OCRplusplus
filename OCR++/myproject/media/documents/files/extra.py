author = "barno"

directory = '/var/www/html/OCR++/myproject/media/documents/'


def comma(y):
	x = y.strip()
	if x[len(x)-1] == ',':
		return "1"
	else:
		return "0"

fi = open(directory + 'test_file.txt','w')

fs = ''

flag = "0"   # to check if a title is already going on
end = 0
with open(directory + 'test.txt','r') as f:
	for line in f:
		abc = line.split()

		if len(abc) == 12:  # if not a blank line

			if abc[4] == fs:
				l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t"+ abc[11] + "\n"
			else:
				fs = abc[4]
				l = "00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\n"
				l = l + abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t"+ abc[11] + "\n"

			fi.write(l);

fi.close()