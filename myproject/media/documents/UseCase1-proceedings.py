import xml.etree.ElementTree as ET
directory = 'myproject/media/documents/'

txxt = ""

f = open(directory + "FOOTNOTEop.txt",'r')
# out = open(directory + 'eval_footnote.txt','w')
xml = f.read()
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for foot in root.findall('footnote'):
    txxt = txxt + foot.text.strip()
f.close()
# out.close()


tree = ET.parse(directory + "Secmap.xml")
root = tree.getroot()

# f = open(directory + 'eval_'+fName.split('.')[0]+'.txt','w')
for section in root.findall('section'):
    heads = section.findall('heading')
    chunks = section.findall('chunk')
    # print "<<section>>"
    # f.write("<<section>>\n")
    if(len(heads)>0):
        # print "Heading: "+heads[0].text
        # f.write("Heading: "+heads[0].text+"\n")
        if "Dataset" in heads[0].text or "DATASET" in heads[0].text or "dataset" in heads[0].text:
		    if(len(chunks)>0):
		        cw = chunks[0].text
		        # print "Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])
		        # f.write("Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])+"\n")
		        txxt = txxt + cw
# f.close()

urls = []

f = open(directory + "URLop.txt",'r')
# out = open(directory + 'eval_url.txt','w')
xml = f.read()
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for URL in root.findall('URL'):
    for url in URL.findall('url'):
        # out.write("<<url>>\n" + url.text.strip() + "\n")
        urls.append(url.text.strip())
f.close()

txxt = txxt.replace(" ","")
txxt = txxt.replace("\n","")
txxt = txxt.replace("\t","")

f = open(directory + "usecase1-proceedings.txt",'a')
for url in urls:
	if url in txxt:
		f.write(url+"\n")
f.write("\n")
f.close()

# print urls
# print txxt