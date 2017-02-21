#!/usr/bin/python

import sys, os, re, getopt
from svg.path import parse_path
from xml.dom import minidom

svgfile = ''

# opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
def main(argv):
	inputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		print '%s -i <inputfile>' % os.path.basename(__file__)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print '%s -i <inputfile>' % os.path.basename(__file__)
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg

	print("inputfile: %s" % inputfile)

	if inputfile != None:
		return inputfile
	else:
		print 'Input file is "%s"' % inputfile
		return None

def doparse(svgfile):
	fd = open(svgfile,'r+')
	lbuff = fd.readlines()
	fd.close()

	svg_str=' '.join(lbuff)

	svg_dom = minidom.parseString(svg_str)
	path_strings = [ path.getAttribute('d') for path in svg_dom.getElementsByTagName('path') ]

	paths=[]
	for s in path_strings:
		paths += parse_path(s)

	return paths

#########################################

if __name__ == "__main__":
	svgfile = main(sys.argv[1:])
	paths = []

	if svgfile != None:
		paths = doparse(svgfile)
	else:
		print("svgfile is None")
		exit()

	pts = []
	if paths != None:
		for p in paths:
			m = re.findall('(start|end)\=\(([0-9\.]+).([0-9\.]+)j\)', str(p), re.DOTALL)
			pts.append( [float(m[0][1]), float(m[0][2]), float(m[1][1]), float(m[1][2])] ) 
			print(p)

	if pts != []:
		for l in pts:
			print(l)