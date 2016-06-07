import xml.etree.ElementTree as ET
import Secmapping
import footnotes
import tables_figures
import url
def main_func():
	directory= ''
	a_file = directory + "input.xml"
	tree = ET.parse(a_file)
	root = tree.getroot()
	footnotes.foot_main(root)
	tables_figures.tab_fig_main(root)
	url.url_main(root)
	return root