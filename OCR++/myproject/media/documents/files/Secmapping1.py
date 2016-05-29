
from __future__ import division

import xml.etree.ElementTree as ET
import unicodedata
import operator
import itertools as iter

import subprocess
import xml.dom.minidom

import roman
import math


files = ["input.xml"]
directory = '/var/www/html/OCR++/myproject/media/documents/'


"""
Create an XML of headings and sections
"""
def generateXML(tree):
    rt = tree.getroot()
    ls = rt.findall('chunk')
    st_chunk = ''
    sp_length = len(ls)
    chunk_stat =0
    xroot = ET.Element("sec_map")
    new_section = ET.SubElement(xroot, "section")
    with open(directory + "finalsec.txt", "r") as f:
        count = 0
        for line in f:
            cols = line.split('\t')
            if len(cols)==9 and cols[8] == '1\n':
                st = ''
                for token in ls[count].findall('token'):
                    st = st + token.text+' '
                st = st.strip('\n')
                if(chunk_stat == 1):
                    ET.SubElement(new_section, "chunk").text = st_chunk
                    chunk_stat = 0
                    st_chunk = ''
                new_section = ET.SubElement(xroot, "section")
                ET.SubElement(new_section, "heading").text = st
            elif(count<sp_length) :
                chunk_stat =1
                for token in ls[count].findall('token'):
                    st_chunk = st_chunk + token.text+' '
                st_chunk = st_chunk.strip('\n')
            count = count + 1
    if chunk_stat == 1:
         ET.SubElement(new_section, "chunk").text = st_chunk
    return xroot


def generateXML_NI(tree):
    rt = tree.getroot()
    ls = rt.findall('chunk')
    st_chunk = ''
    sp_length = len(ls)
    chunk_stat =0
    xroot = ET.Element("sec_map")
    new_section = ET.SubElement(xroot, "section")
    with open(directory + "finalsec_NI.txt", "r") as f:
        count = 0
        for line in f:
            cols = line.split('\t')
            if len(cols)==9 and cols[8] == '1\n':
                st = ''
                for token in ls[count].findall('token'):
                    st = st + token.text+' '
                st = st.strip('\n')
                if(chunk_stat == 1):
                    ET.SubElement(new_section, "chunk").text = st_chunk
                    chunk_stat = 0
                    st_chunk = ''
                new_section = ET.SubElement(xroot, "section")
                ET.SubElement(new_section, "heading").text = st
            elif(count<sp_length) :
                chunk_stat =1
                for token in ls[count].findall('token'):
                    st_chunk = st_chunk + token.text+' '
                st_chunk = st_chunk.strip('\n')
            count = count + 1
    if chunk_stat == 1:
         ET.SubElement(new_section, "chunk").text = st_chunk
    return xroot




"""
Token features as decimals
Special Sections    - 6
Single word chunk   - 5
Tables/Figures      - 0
Section Number      - 1
UpperCase token     - 2
Special Symbols     - 3
Rest                - 4
"""

def token_features(y):
    x=y.strip()
    parts=x.split('.')
    if(x=="Abstract" or x== "ABSTRACT" or x=="Acknowledgement" or x== "ACKNOWLEDGEMENT" or x=="References" or x== "Reference" or x == "REFERENCE" or x=="REFERENCES" or x=="Acknowledgements" or x== "ACKNOWLEDGEMENTs"):
        return "6"
    if(x=="$$$"):
        return "5"
    if x=="Table" or x=="TABLE" or x=="Figure" or x=="FIGURE" or x=="Fig.":
        return "0"
    p_len = len(parts)
    if(p_len==1):
        if(x.isdigit() and 1<=int(x)<=20):
            return "1"
    if(p_len==2 or p_len==3):
        if(parts[0].isdigit() and 1<=int(parts[0])<=20):
            if(parts[1]=='' or (parts[1].isdigit() and int(parts[1])<=20)):
                if(p_len==2):
                    return "1"
                if(parts[1].isdigit() and int(parts[1])<=20 and parts[2]==''):
                    return "1"
    if(p_len==1 or (p_len==2 and parts[1]=='')):
        try:
            val = roman.fromRoman(parts[0].upper())
            if(val<=20):
                return "1"
        except:
            pass
        if((len(parts[0])==1 and 'A'<=parts[0]<='Z') or (len(parts[0])==3 and parts[0][0]=='(' and parts[0][2]==')' and parts[0][1].isalpha() and parts[0][1].isupper()) or (len(parts[0])==2 and parts[0][1]==')' and parts[0][0].isalpha() and parts[0][0].isupper())):
            if(p_len==1 or (p_len==2 and parts[1]=='')):
                return "1"
    if x[0].isupper():
        return "2"
    if (not(parts[0].isalpha() or parts[0].isdigit())):
        return "3"
    return "4"


"""
Main function for section mapping
includes the pdftoxml file and the Path to the
file as parameters, path is defaulted to be the
current directory
"""

# def secmap(ff, path=""):
for ff in files:
    tree = ET.parse(directory+ff)
    root = tree.getroot()

    preYLOC = None
    yDiff={}
    fontSizes = {}

    for pages in root.findall('PAGE'):
        preYLOC=0
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                try:
                    fontSizes[round(abs(float(token.attrib['font-size'])))]=fontSizes.get(round(abs(float(token.attrib['font-size']))),0)+1
                    if(preYLOC is None):
                        preYLOC=float(token.attrib['y'])
                    yDiff[round(abs(float(token.attrib['y'])-preYLOC))]=yDiff.get(round(abs(float(token.attrib['y'])-preYLOC)),0)+1
                    preYLOC=float(token.attrib['y'])
                except:
                    pass

    modalFS = 0
    # Find Modal Font size
    for FS in fontSizes.keys():
        if(modalFS == 0):
            modalFS = FS
            continue
        if(fontSizes[FS]>fontSizes[modalFS]):
            modalFS=FS

    # Finding modal Y difference
    new_l = sorted(yDiff.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]
    x_l = []
    # print(new_l)
    for k in new_l:
        if(k[0]>6.0):
            x_l.append(k)
    new_l=x_l

    x_l=[]
    mode=new_l[0][1]
    for k in new_l:
        if(not(k[1]<=mode/2 or abs(new_l[0][0]-k[0])>=4)):
            x_l.append(k)

    new_l=x_l
    # print(new_l)
    del x_l

    limit = max([x[0] for x in new_l])+1
    # print(limit)


    # Create new XML file for Chunks
    preYLOC = None
    xroot = ET.Element("Document")
    chunk = ET.SubElement(xroot, "chunk")
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(word and len(word.replace(' ',''))>0):
                    if(preYLOC is None):
                        preYLOC = float(token.attrib['y'])
                        ET.SubElement(chunk, "token", font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word
                        continue
                    if(abs(float(token.attrib['y'])-preYLOC)>=limit):
                        chunk = ET.SubElement(xroot, "chunk")
                    preYLOC = float(token.attrib['y'])
                    ET.SubElement(chunk, "token", font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word

    tree = ET.ElementTree(xroot)
    # tree.write(ff+"_res.xml")
    tree_NI = tree

    newxroot = ET.Element("Document")
    ET.SubElement(newxroot, "chunk")

    preFS = None

    root = tree.getroot()

    # Refining chunks to strip leading headings FOR INDEXED PDFS
    for chunks in root.findall('chunk'):
        chunk = ET.SubElement(newxroot, "chunk")
        count = 0
        stat = 0
        if(len(chunks)>20):
            stat = 1
        for token in chunks.findall('token'):
            if(count < 15 and preFS is not None and float(token.attrib["font_size"]) < preFS and stat==1 ):
                chunk = ET.SubElement(newxroot, "chunk")
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
            else:
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
                count  = count + 1
            preFS = float(token.attrib['font_size'])

    tree = ET.ElementTree(newxroot)
    tree.write(directory + ff+"_fin.xml")


    newxroot = ET.Element("Document")
    ET.SubElement(newxroot, "chunk")

    root = tree_NI.getroot()
    preFS = None
    for chunks in root.findall('chunk'):
        chunk = ET.SubElement(newxroot, "chunk")
        count = 0
        stat = 0
        if(len(chunks)>20):
            stat = 1
        for token in chunks.findall('token'):
            if count < 15 and preFS is not None and preFS < float(token.attrib["font_size"]) and stat==1:
                chunk = ET.SubElement(newxroot, "chunk")
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
            else:
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
                count  = count + 1
            preFS = float(token.attrib['font_size'])

    tree_NI = ET.ElementTree(newxroot)
    tree_NI.write(directory + ff+"_fin_NI.xml")







    # Generating the final txt config file

    # items = iter.izip(iter.islice(entries, 1, None), entries)
    # for chunk1,chunk2,chunk3,chunk4 in
    #


    f = open(directory + ff.split('.')[0]+'_out.txt','w')

    newxroot = tree.getroot()

    for achunk in newxroot.findall('chunk'):
        boldness = 0
        fsize = 0
        tokens = achunk.findall('token')
        if(len(tokens)==0):
            f.write('xxx\t0\t0\t0.0\t0\t0\t0\t0\n')
            continue
        elif(len(tokens) ==1):
            tok1 = '$$$'
            tok2 = tokens[0].text
        else:
            tok1 = tokens[0].text
            tok2 = tokens[1].text
        tcount = len(tokens)
        for t in tokens:
            if(t.attrib['bold']=="yes"):
                boldness=boldness+1
            fsize = fsize + float(t.attrib['font_size'])
        boldness = round(boldness/tcount,2)
        fsize = (fsize/tcount)/modalFS
        tcount = math.floor(tcount / 16)
        f.write(tok1+"\t"+tok2+"\t"+str(int(tcount))+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

    f.close()
    subprocess.call("crf_test -m " + directory + "files/mod2 " + ff.split('.')[0]+'_out.txt'+" > " + directory + "finalsec.txt", shell=True)
    f = open(directory + ff.split('.')[0]+'_out_NI.txt','w')
    newxroot = tree_NI.getroot()

    for achunk in newxroot.findall('chunk'):
        boldness = 0
        fsize = 0
        tokens = achunk.findall('token')
        if(len(tokens)==0):
            f.write('xxx\t0\t0\t0.0\t0\t0\t0\t0\n')
            continue
        elif(len(tokens) ==1):
            tok1 = '$$$'
            tok2 = tokens[0].text
        else:
            tok1 = tokens[0].text
            tok2 = tokens[1].text
        tcount = len(tokens)
        for t in tokens:
            if(t.attrib['bold']=="yes"):
                boldness=boldness+1
            fsize = fsize + float(t.attrib['font_size'])
        boldness = round(boldness/tcount,2)
        fsize = (fsize/tcount)/modalFS
        tcount = math.floor(tcount / 16)
        f.write(tok1+"\t"+tok2+"\t"+str(int(tcount))+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

    f.close()


    # subprocess.call("crf_test -m mod_10_1 " + ff.split('.')[0]+'_out.txt'+" > " + directory + "finalsec_NI.txt", shell=True)
    subprocess.call("crf_test -m " + directory + "files/model_4_1_16 " + ff.split('.')[0]+'_out.txt'+" > " + directory + "finalsec_NI.txt", shell=True)

    # cc = ET.tostring(secTree, 'utf-8')
    # reparsed = minidom.parseString(cc)
    # print reparsed.toprettyxml(indent="\t")
    # subprocess.call("rm "+ff.split('.')[0]+".txt "+ff.split('.')[0]+'_out.txt', shell=True)





    count =0
    count_NI =0
    with open(directory+"finalsec.txt", "r") as f:

        for line in f:
            cols = line.split('\t')
            if len(cols)==9 and cols[8] == '1\n':
                count = count +1

    with open(directory+"finalsec_NI.txt", "r") as f:

        for line in f:
            cols = line.split('\t')
            if len(cols)==9 and cols[8] == '1\n':
                count_NI = count_NI +1

    if count >= count_NI :
        # print("Indexed")
        secTree = generateXML(tree)
    else :
        # print("Non-Indexed")
        secTree = generateXML_NI(tree)

    cc =  ET.tostring(secTree, 'utf-8')
    reparsed = xml.dom.minidom.parseString(cc)
    print reparsed.toprettyxml(indent="\t")
    # print "Done!"
