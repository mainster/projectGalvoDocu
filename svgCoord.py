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
from __future__ import print_function
import sys, os, re, getopt, math
import numpy as np
from shutil import copyfile
from svg.path import parse_path
from xml.dom import minidom
from lxml import etree
# from xml.dom.minidom import toprettyxml 
from collections import namedtuple  
from numpy.lib.recfunctions import append_fields
# from xml.etree.ElementTree import Element, SubElement, Comment, tostring
# from ElementTree_pretty import prettify

#-------------------------------------------------------------------------------
## Template string of circle node marker shape
##
circleTempStr=['<circle',
	'\tstyle="opacity:<OPACITY>;fill:<FILL_COLOR>;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"',
	'\tid="nodeMarker_<UID>"',
	'\tcx="<CX>"',
	'\tcy="<CY>"',
	'\tr="<R>" />']

R='{http://www.w3.org/2000/svg}'

#-------------------------------------------------------------------------------
## @brief      Provides a storage class for path object payloads.
##
class Paths:
	def __init__(self, name, path):
		self.name = name
		self.lines = []
		self.nodes = []

		for n in path:
			m = re.findall('(start|end)\=\((-?[0-9\.]+)([+-][0-9\.]+)j\)', str(n), re.DOTALL)
			self.lines.append((
				float(m[0][1]), float(m[0][2]), 
				float(m[1][1]), float(m[1][2])) )

		# Derive nodes from line objects
		[ (self.nodes.append((line[0], line[1])),
			self.nodes.append((line[2], line[3]))) for line in self.lines ]

	def getLines(self):
		return self.lines

	def getNodes(self):
		return self.nodes

#-------------------------------------------------------------------------------
## @brief      Class for inkscape svg objects style attributes.
##
class Style_t:
	#------------------------------------------------------------------------------
	## @brief      Constructs the style attributes object.
	## @param      self      Instance of style attributes object.
	## @param      attrStr   Complete <path ... style: attribute string.
	##
	def __init__(self, pathId, attrStr):
		if np.ndim(attrStr) > 0:
			print("np.ndim(attrStr) > 0"); exit()

		self.pathId = pathId
		vps=[]; 
		# Value-pair list comprehension
		[ vps.append(vp.split(':')) for vp in attrStr.split(';') ] 
		# Instantiate style attributes dictionary
		self.styAttrs = dict(vps)

	#------------------------------------------------------------------------------
	## @brief      Sets/changes attributes.
	## @param      self   Instance of style attributes object.
	## @param      vp     Value-pair string, e.g. 'stroke:#ff0000'
	## @param      fs     Custom field separator
	##
	def setAttr(self, vp1, vp2fs=':'):
		if vp2fs == ':':		
			if len(vp1.split(vp2fs)) == 2:
				self.styAttrs[vp1.split(vp2fs)[0]] = vp1.split(vp2fs)[1]
			else: 
				print("Not a valid value-pair")
		else:
			self.styAttrs[vp1] = vp2fs;


	#------------------------------------------------------------------------------
	## @brief      Gets the value for selected attribute.
	## @param      self       Instance of style attributes object.
	## @param      attrName   The attribute name
	## @param      asVp       Set flag true for sinle string vp return is required 
	## @return     The attribute.
	##
	def getAttr(self, attrName, asVp=False):
		if asVp:
			return str(attrName +':'+ self.styAttrs[vp.split(fs)[0]])
		return self.styAttrs[vp.split(fs)[0]]

	def getAttrList(self):
		return self.styAttrs.keys()

	def getAttrStr(self):
		astr = []
		[ astr.append('%s:%s' % (v, p)) for v, p in self.styAttrs.iteritems() ]
		return ';'.join(astr)

	def dumpObj(self):
		for k in range(len(self.styAttrs.keys())):
			print("(%s : %s)" % (self.styAttrs.keys()[k], self.styAttrs.values()[k]))

#-------------------------------------------------------------------------------
## @brief      Pretty prints the node buffer.
## @param      data   Buffer which holds lines or nodes from svg paths.
##
def prettyPrint(data):
	# Find the largest x or y value in whole nodes buffer
	
	try:
		MAX = max( [ max(line) for line in data ] )
	except:
		print("Exception max([])")
		MAX = 1000

	exp = 1;

	# Ceil to next decade
	while math.ceil(MAX/10**exp) != 1.0:	
		exp += 1

	# decimal places (2) + dot separator (1) = 3  
	formatstr = '%%%i.%if' % (exp+2+1, 2)

	# Format/round data buffer
	data = [[ formatstr % node for node in line ] for line in data ]
	for el in data: 
		print(el)

#-------------------------------------------------------------------------------
## @brief      Return a pretty-printed XML string for the Element.
## @param      elem   The element to prettify
## @return     Pretty XML element.
##
def prettyElem(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

#-------------------------------------------------------------------------------
## @brief      Returns xml tag of a template bed node marker shape.
## @param      cx          The nodes x-coordinate.
## @param      cy          The nodes y-coordinate.
## @param      uid         An uniq node-marker-identifier, integer.
## @param      r           Node marker radius.
## @param      opacity     Node marker opacity.
## @param      fillColor   Node marker fill color.
## @return     Node marker xml tag.
##
def nodeMarker(cx, cy, uid, r=2, opacity=.8, fillColor='#ff0000'):
	return [ p
	.replace('<CX>', str(cx))
	.replace('<CY>', str(cy))
	.replace('<UID>', str(uid))
	.replace('<R>', str(r)) 
	.replace('<OPACITY>', str(opacity))
	.replace('<FILL_COLOR>', str(fillColor)) 
	for p in circleTempStr ]

#-------------------------------------------------------------------------------
## @brief      Acts as parser core. Creates buffers containing XML tag payload.
## @param      infile   The svg file whose nodes are to be marked.
## @return     mPaths: 	Holds all node coordinates of a defined svg path. offs:
##             Returns transformation/translation coordinates if corresponding
##             tags wherefound, else (0, 0)
##
def doParse(infile):
	fd = open(infile,'r+')
	lbuff = fd.readlines()
	fd.close()
	svg_dom = minidom.parseString(' '.join(lbuff))

	# Request for the perhaps-attribute: 'offs' or transform, if therei s a <g> tag present!
	offs = (0, 0)
	if svg_dom.getElementsByTagName('g'):
		if max([ g.hasAttribute("transform") for g in svg_dom.getElementsByTagName('g') ]):
			rawTransform = [ g.hasAttribute("transform") for g in svg_dom.getElementsByTagName('g') ]
			m = re.findall('translate\(([-+]?[0-9\.]+)\,([-+]?[0-9\.]+)\)', rawTransform[0], re.DOTALL)
			offs = [ float(m[0][0]), float(m[0][1]) ]
	print("No xml-tag <g> found!")

	# Get all path attributes and the paths identifier	
	rawPathsIds = [ (path.getAttribute('d'), 
		path.getAttribute('id')) for path in svg_dom.getElementsByTagName('path') ]
	# Create Path() class instance
	mPaths = []
	[ mPaths.append( Paths(s[1], parse_path(s[0])) ) for s in rawPathsIds ]
	return (mPaths, offs)

#-------------------------------------------------------------------------------
## @brief      Manipulate path attributes in xml source tree.
## @param      infile    The svg input file.
## @param      valPair   Value-pair which should be modified
## @param      suffix    Optional output file suffix
## @return     Outfile pathe/name.
##
def styleManipulate(infile, valPair='stroke-opacity:0.5', suffix=''):
	tree = etree.parse(infile)
	root = tree.getroot()
	pStyles = dict()
	baseElems = [root]

	# Check if <g> element encloses all other <path> elements!
	[ baseElems.append(g) for g in root.findall(R + 'g') ]
	print("be elements: ", [ g.tag.replace(R, '') for g in baseElems ] )

	for be in baseElems:
		# Create dict with pathID keys and style object as value
		for path in be.findall(R + 'path'):
			# Create a Style_t instance for each path tag in xml source tree.
			pStyles[ path.get('id') ] = Style_t(path.get('id'), path.get('style'))
			pStyles[ path.get('id') ].setAttr( valPair )

		for path in be.findall(R + 'path'):
			ID = path.get('id')
			path.set('style', pStyles[ID].getAttrStr())

	# Write back the modified xml tree
	outfile = os.path.splitext(infile)[0] + suffix + os.path.splitext(infile)[1]

	with open(outfile, 'w') as fd:
		fd.write(etree.tostring(tree, pretty_print=True, encoding='utf8'))
	return outfile

#-------------------------------------------------------------------------------
## @brief      Places a node marker on each node.
## @param      infile       The svg file whose nodes are to be marked.
## @param      mPaths        Paths class instance.
## @param      MARKER_SIZE   Size of node markers [px].
## @return     -
##
def placeNodeMarker(infile, mPaths, MARKER_SIZE = 3, suffix=''):
	SVG_END_TAG='</svg>\n'
	# Open svg, read lines to buffer, close file	
	fd = open(infile,'r+')
	lines = fd.readlines()
	fd.close()

	# Get index of svg-end tag
	idx = lines.index(SVG_END_TAG)
	
	if not idx: 
		print("svg end tag not found!"); exit();
	print("svg end tag found at line %d" % idx)

	for p in mPaths:
		for node in p.getNodes():
			circleMark = nodeMarker(node[0], node[1], 1000 + 1, MARKER_SIZE)
			for l in range(len(circleMark)):
				lines.insert(idx+l, "\t" + circleMark[l] + "\n")

	fd = open(os.path.splitext(infile)[0] + 
		suffix + os.path.splitext(infile)[1], 'w')
	fd.writelines(lines)
	fd.close()

#-------------------------------------------------------------------------------
## @brief      Input argument parsing.
## @param      argv   List of input arguments.
## @return     Input file path, doPretty flag.
##
def main(argv):
	inputfile = ''
	doPretty = False
	cmdUsage = '%s -i <inputfile> [-p]' % os.path.basename(__file__)
	try:
		onodes, args = getopt.getopt(argv,"hi:p",["ifile=", "pretty"])
	except getopt.GetoptError:
		print(cmdUsage)
		sys.exit(2)

	for opt, arg in onodes:
		if opt == '-h':
			print(cmdUsage)
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-p", "--pretty"):
			doPretty = True

	if not os.path.isfile(inputfile):
		print('Input file "%s" not valied!' % inputfile)

	return (inputfile, doPretty)

#-------------------------------------------------------------------------------
## Script run.
##
if __name__ == "__main__":

	mPaths = []
	try: 
		(infile, doPretty) = main(sys.argv[1:])	# Parse input arguments
		(mPaths, offs) = doParse(infile)			# Get paths from vector graphic
	except: 
		if not infile: print("Argument for -i not given"); exit()
		if not mPaths:	print("Error, no paths or bad -i argument"); exit()

	if offs: 
		print("offs attr: %f, %f" % (offs[0], offs[1]))

	# Manipulate path style attributes
	ofile = styleManipulate(infile, 'stroke-opacity:0.3', '_mod')

	# Place node markers into xml-tree of selected infile.
	placeNodeMarker(ofile, mPaths, 2, '')

	# Pretty print(nodes to console.)
	if doPretty:
		for path in mPaths:
			prettyPrint(path.getLines())

		lin = []
		[ lin.append(len(path.getLines())) for path in mPaths ] 

		print("Paths count: %i" % len(mPaths))
		print("Lines count: %i" % sum(lin))	
		print("Nodes count: %i" % (sum(lin)+len(mPaths)))
###############################################################################
## 	Script end.
###############################################################################

