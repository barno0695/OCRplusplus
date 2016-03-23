import xml.etree.ElementTree as ET
directory = "/var/www/html/OCR++/myproject/media/documents/"
f = open(directory + "input_cit2ref.xml",'r')
out = open(directory + 'eval_cit2ref.xml','w')
xml = '<root>' + f.read() + '</root>'
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
#for refs in root.findall('Reference'):
#    out.write("<<Reference>><<" + refs.attrib['id'] + ">> " + refs.text.strip() + "\n")
for documents in root.findall('Document'):
	for all_cits in documents.findall('Cit2ref'):
		for cits in all_cits.findall('cit2ref'):
			out.write("<<cit2ref>>\n" + "Citation : " + cits.text.strip() + "\n" + "Reference  : \n" + cits.attrib['reference'] + "\n");
f.close()
out.close()
