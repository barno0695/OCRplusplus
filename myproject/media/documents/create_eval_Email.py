import xml.etree.ElementTree as ET
directory = "myproject/media/documents/"
f = open(directory + "input_Allmails.txt",'r')
out = open(directory + 'eval_emails.txt','w')
xml = '<root>' + f.read() + '</root>'
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for mail in root.findall('email'):
    out.write("<<Email>> \n" + mail.text.strip() + "\n")
f.close()
out.close()
