#!/usr/bin/python
###############################################################################
## File:	svgCoord.py
###############################################################################
## 
## Author:	Manuel Del Basso (mainster)
## Email:	manuel.delbasso<ta>gmail.com
## Date:	11/2016
##  
## This file is a part of project "XY-GalvoScanner" and is used to extract 
## node coordinates from vector graphics xml description.
## 
## Output formats:
## 		(x0, y0, beam0), 	# Node 0 X- Y coordinates, beam interrupter state    
## 		(x1, y1, beam1), 	# Node 1 X- Y coordinates, beam interrupter state    
## 		....
##
## PlaceNodeMarker:
## ----------------
## This script also provides simple node manipulation functionality. 
## To visualize the presents of all nodes on multiple paths, a node marker 
## shape (red dot or something) will be placed to coordinates of all nodes. 
## 
###############################################################################
import sys, os, re, getopt, math
import numpy as np
from svg.path import parse_path
from xml.dom import minidom
from shutil import copyfile

SVG_END_TAG="</svg>\n"
svgfile = ''

circleTempStr=['<circle',
	'\tstyle="opacity:.8;fill:#ff0000;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"',
	'\tid="path<UID>"',
	'\tcx="<CX>"',
	'\tcy="<CY>"',
	'\tr="<R>" />']

# Returns template based node marker 
def nodeMarker(cx, cy, uid, r=2):
	return [ p
	.replace('<CX>', str(cx)).replace('<CY>', str(cy))
	.replace('<UID>', str(uid)).replace('<R>', str(r)) 
	for p in circleTempStr ]

def main(argv):
	inputfile = ''
	try:
		onodes, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		print '%s -i <inputfile>' % os.path.basename(__file__)
		sys.exit(2)

	for opt, arg in onodes:
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

def doParse(svgfile):
	fd = open(svgfile,'r+')
	lbuff = fd.readlines()
	fd.close()
	svg_dom = minidom.parseString(' '.join(lbuff))
	# Get all path attributes	
	rawPathsIds = [ (path.getAttribute('d'), 
		path.getAttribute('id')) for path in svg_dom.getElementsByTagName('path') ]

	# Request for perhaps-attribute 'offs'
	rawTransform = [ path.getAttribute('transform') for path in svg_dom.getElementsByTagName('g') ]

	if rawTransform:
		m = re.findall('translate\(([-+]?[0-9\.]+)\,([-+]?[0-9\.]+)\)', rawTransform[0], re.DOTALL)
		offs = [ float(m[0][0]), float(m[0][1]) ]
	else: 
		offs = (0, 0)

	paths = []
	if rawPathsIds:	
		for s in rawPathsIds:			
			paths += parse_path(s[0])
			# ma = re.findall('pathRightEye', str(s[1]))
			# if ma != []: print(s)
	else:
		paths = None

	return (paths, offs)

##
## @brief      Places a node marker on each node.
##
## @param      svgfile       The svg file whose nodes are to be marked.
## @param      nodes         List of xy-tupels where each tupel represents node
##                           coordinates.
## @param      MARKER_SIZE   Size of node markers [px].
##
## @return     -
##
def placeNodeMarker(svgfile, nodes, MARKER_SIZE = 3):
	# Open svg, read lines to buffer, close file	
	fd = open(svgfile,'r+')
	lines = fd.readlines()
	fd.close()

	# New file, copy and open in write mode
	newSvg = os.path.splitext(svgfile)[0] + "_mod" + os.path.splitext(svgfile)[1]
	if os.path.isfile(newSvg): 
		os.remove(newSvg)
	copyfile(svgfile, newSvg)
	fd = open(newSvg,'w')

	# Get index of svg-end tag
	idx = lines.index(SVG_END_TAG)
	
	if not idx: 
		print("svg end tag not found!"); fd.close(); exit();

	print("svg end tag found at line %d" % idx)

	for lSeg in range(len(nodes)):
		circleMark = nodeMarker(nodes[lSeg][0], nodes[lSeg][1], 1000 + lSeg, MARKER_SIZE)
		for l in range(len(circleMark)):
			lines.insert(idx+l, "\t" + circleMark[l] + "\n")

	fd.writelines(lines)
	fd.close()

#########################################

if __name__ == "__main__":
	paths = []
	try:
		svgfile = main(sys.argv[1:])
		# Get paths from vector graphic
		(paths, offs) = doParse(svgfile)
	except:
		if not svgfile: print("Argument for -i not given"); exit()
		if not paths:	print("Error, no paths or bad -i argument"); exit()
		
	if offs: 
		print("offs attr: %f, %f" % (offs[0], offs[1]))

	lines = []
	# For each [start=xxx, end=xxx] tupel, ... 
	for p in paths:
		# Regex x+y float values for a lines start and end node.  
		m = re.findall('(start|end)\=\((-?[0-9\.]+)([+-][0-9\.]+)j\)', str(p), re.DOTALL)
		# Add transformation offset.
		lines.append([
			float(m[0][1])+offs[0], float(m[0][2])+offs[1], 
			float(m[1][1])+offs[0], float(m[1][2])+offs[1]])

	if not lines: print("Empty lines buffer!"); exit()

	# Extract single point objects (x/y) from svg-line buffer ((x1/y1), (x2/y2))  
	pts = []
	for line in lines:
		pts.append( (line[0], line[1]) )
		pts.append( (line[2], line[3]) )


	# Place node markers in svgfile
	placeNodeMarker(svgfile, pts, 2)

	################
	# Pretty print:
	################

	# Find the largest x or y value in whole nodes buffer
	MAX = max([ max(line) for line in lines ]); 
	exp = 1;

	# Ceil to next decade
	while math.ceil(MAX/10**exp) != 1.0:	
		exp += 1

	# decimal places (2) + dot separator (1) = 3  
	formatstr = '%%%i.%if' % (exp+2+1, 2)

	# Format/round lines buffer
	lines = [[ formatstr % node for node in line ] for line in lines ]

	for node in lines:
		print(node)

