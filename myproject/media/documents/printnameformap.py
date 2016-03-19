from __future__ import division

import xml.etree.ElementTree as ET
directory = 'myproject/media/documents/'


# """
# Create an summary file of author names
# """
def genFile(fName, path=""):
    tree = ET.parse(directory + "TitleAuthor.xml")
    root = tree.getroot()
    f = open(directory + 'title_author.txt','w')
    for author in root.findall('name'):
        fn = author.findall('first_name')
        mn = author.findall('middle_name')
        ln = author.findall('last_name')
        # print "<<section>>"
        # f.write("<<name>>\n")
        # print fn[0].text.split()[0]
        if(len(fn)>0):
            f.write("#f "+fn[0].text.split()[0]+"\n")
        if(len(mn)>0):
            f.write("#m "+mn[0].text.strip('\t').strip('\n').strip('\t')+"\n")
        if(len(ln)>0):
            f.write("#l "+ln[0].text.split()[0]+"\n")
    f.close()
    # print "Done!!!"


"""Demo call"""
genFile("TitleAuthor.xml")