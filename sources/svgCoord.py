#!/usr/bin/python
########################################
# File: svgCoord.py
########################################
#
# Author:   Manuel Del Basso (mainster)
# Email:    manuel.delbasso<ta>gmail.com
# Date: 11/2016
#
# This file is a part of project "XY-GalvoScanner" and is used to extract
# node coordinates from vector graphics xml description.
#
# Output formats:
#       (x0, y0, beam0),    # Node 0 X- Y coordinates, beam interrupter state
#       (x1, y1, beam1),    # Node 1 X- Y coordinates, beam interrupter state
#       ....
#
# PlaceNodeMarker:
# ----------------
# This script also provides simple node manipulation functionality.
# To visualize the presents of all nodes on multiple paths, a node marker
# shape (red dot or something) will be placed to coordinates of all nodes.
#
########################################
from __future__ import print_function
import sys
import os
import re
import getopt
import math
import numpy as np
from svg.path import parse_path
from xml.dom import minidom
from lxml import etree
from mdLibs import mdosd as osd
from abc import abstractmethod
from pprint import pprint

if sys.version_info[0] == 2:
    sys.path.insert(0, '/home/mainster/CODES_local/pythons/swampy-2.1.7/swampy/')
else:
    sys.path.insert(0, '/home/mainster/CODES_local/pythons/swampy-2.1.5/')

from Lumpy import Lumpy
lumpy = Lumpy()
lumpy.make_reference()

# from shutil import copyfile
# from collections import namedtuple
# from numpy.lib.recfunctions import append_fields
# from subprocess import call


# Aliases
dim = np.shape

# ---------------------------------------------------------------
# Template string of circle node marker shape
#
circleTempStr = ['<circle',
'\tstyle="opacity:<OPACITY>;fill:<FILL_COLOR>;fill-opacity:1;'
'fill-rule:nonzero;stroke:none;stroke-width:1;stroke-linecap:'
'round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dasho'
'ffset:0;stroke-opacity:1"',
'\tid="nodeMarker_<UID>"',
'\tcx="<CX>"',
'\tcy="<CY>"',
'\tr="<R>" />']

R = '{http://www.w3.org/2000/svg}'
MATLAB_PRJ = '/home/mainster/CODES_local/matlab_workspace'

DEBUG = False


class dprint:
    def __init__(self, arg, opt=None):
        global DEBUG
        if DEBUG:
            print(os.path.basename(__file__), end=' ')
            if opt is not None:
                print(arg, opt)
            else:
                print(arg)


class Paths:
    def __init__(self, name, path, offs=(0, 0)):
        ''' Provides a storage class for path object payloads. '''
        self.name = name
        self.valid = True
        self.lines = []
        self.nodes = []

        # Check for empty path
        if len(path) is 0:
            dprint("Empty path, id: %s " % self.name)
            self.valid = False
        else:
            for n in path:
                m = re.findall('(start|end)\=\((-?[0-9\.]+)([+-][0-9\.]+)j\)', str(n), re.DOTALL)
                self.lines.append((
                    float(m[0][1]) + offs[0], float(m[0][2]) + offs[1],
                    float(m[1][1]) + offs[0], float(m[1][2]) + offs[1]))

            # Derive nodes from line objects
            [(self.nodes.append((line[0], line[1])),
                self.nodes.append((line[2], line[3]))) for line in self.lines]

    def getLines(self):
        return self.lines

    def getNodes(self):
        return self.nodes

    def isValid(self):
        return self.valid


# ------------------------------------------------------------------------------
# @brief      Class for inkscape svg objects style attributes.
#
class Style_t:
    # -----------------------------------------------------------------------------
    # @brief      Constructs the style attributes object.
    # @param      self      Instance of style attributes object.
    # @param      attrStr   Complete <path ... style: attribute string.
    #
    def __init__(self, pathId, attrStr):
        if np.ndim(attrStr) > 0:
            print("np.ndim(attrStr) > 0")
            exit()

        self.pathId = pathId
        vps=[]
        # Value-pair list comprehension
        [ vps.append(vp.split(':')) for vp in attrStr.split(';') ]
        # Instantiate style attributes dictionary
        self.styAttrs = dict(vps)

    # -----------------------------------------------------------------------------
    # @brief      Sets/changes attributes.
    # @param      self   Instance of style attributes object.
    # @param      vp     Value-pair string, e.g. 'stroke:#ff0000'
    # @param      fs     Custom field separator
    #
    def setAttr(self, vp1, vp2fs=':'):
        if vp2fs == ':':
            if len(vp1.split(vp2fs)) == 2:
                self.styAttrs[vp1.split(vp2fs)[0]] = vp1.split(vp2fs)[1]
            else:
                print("Not a valid value-pair")
        else:
            self.styAttrs[vp1] = vp2fs;


    # -----------------------------------------------------------------------------
    # @brief      Gets the value for selected attribute.
    # @param      self       Instance of style attributes object.
    # @param      attrName   The attribute name
    # @param      asVp       Set flag true for sinle string vp return is required
    # @return     The attribute.
    #
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

# ------------------------------------------------------------------------------
# @brief      Class to provide an output generator (prettyPrint, write log, write header)
#
class Output(object):
    def __init__(self, mPaths, logfile=None, incfile=None):
        self.logfile = logfile
        self.incfile = incfile
        self.lines = []
        self.linesPretty = []
        self.nlines = []

        [(self.lines.append(path.getLines()),
            self.nlines.append(len(path.getLines()))) for path in mPaths]
        self.nlines = sum(self.nlines)

        # Find max 2d vector element
        self.max = [max(line) for line in self.lines]
        while dim(self.max):
            self.max = max(self.max)
        print('max: %i' % self.max)

        # decimal places (2) + dot separator (1) = 3
        formatstr = '%%%i.%if' % (self.getPreceedSpace(self.max)+2+1, 2)

        # Format/round data buffer
        # self.linesPretty = [[formatstr % node for node in line] for line in self.lines[0]]
        for path in self.lines:
            for pline in path:
                line = []
                [line.append(formatstr % node) for node in pline]
                self.linesPretty.append(line)

    # Ceil to next decade
    def getPreceedSpace(self, value):
        # print('len: %i  shape:' % len(value), np.shape(value))
        exp = 1;
        while math.ceil(self.max/10**exp) != 1.0:
            exp += 1
        return exp

    @abstractmethod
    def out(self, numberLines=False):
        # self.numberLines = numberLines
        pass

# ------------------------------------------------------------------------------
# @brief      Pretty prints the node buffer.
#
class PrettyPrint(Output):
    def out(self, numberLines=False):
        if numberLines:
            prefix = '%%%ii:' % self.getPreceedSpace(len(self.linesPretty))
            for k in range(len(self.linesPretty)):
                print(prefix % (k+1), self.linesPretty[k])
        else:
            for line in self.linesPretty:
                print(line)

# ------------------------------------------------------------------------------
# @brief      Writes a log file to filesystem
#
class CreateLog(Output):
    def out(self):
        try:
            fd = open(self.logfile, 'w')
            for line in self.linesPretty:
                fd.write('\t'.join(line) + '\n')

            fd.close()
            osd.ok('%s' % self.logfile, 'Logfile successfully written').send()
        except:
            osd.warn('Exception while writing logfile').send()

class CreateInclude(Output):
    def out(self):
        try:
            fd = open(self.incfile, 'w')

            fd.write(
                """#include <stdio.h>
#include <stdint.h>

typedef float node_t[2];      /* A nodes X- and Y- values */
typedef node_t lseg_t[2];     /* A line segment is defined by 2 nodes (x1,y1),(x2,y2) */
typedef lseg_t svg_t[2];      /* An array of line segments */


const lseg_t gnu[ ] = {
""")

            for k in range(len(self.linesPretty)):
                line = self.linesPretty[k]
                if k < len(self.linesPretty) - 1:
                    fd.write('\t{{ %s, %s }, { %s, %s }},\n'
                        % (str(line[0]), str(line[1]), str(line[2]), str(line[3])))
                else:
                    fd.write('\t{{ %s, %s }, { %s, %s }}\n};\n'
                        % (str(line[0]), str(line[1]), str(line[2]), str(line[3])))

            fd.close()
            osd.ok('%s' % self.incfile, 'IncFile successfully written').send()
        except (ValueError, TypeError) as e:
            print('Exception while writing incfile:\n%s' % e.message)
            osd.warn('Exception while writing incfile:\n%s' % e.message).send()


# ------------------------------------------------------------------------------
# @brief      Returns xml tag of a template bed node marker shape.
# @param      cx          The nodes x-coordinate.
# @param      cy          The nodes y-coordinate.
# @param      uid         An uniq node-marker-identifier, integer.
# @param      r           Node marker radius.
# @param      opacity     Node marker opacity.
# @param      fillColor   Node marker fill color.
# @return     Node marker xml tag.
#
def nodeMarker(cx, cy, uid, r=2, opacity=.8, fillColor='#ff0000'):
    return [ p
    .replace('<CX>', str(cx))
    .replace('<CY>', str(cy))
    .replace('<UID>', str(uid))
    .replace('<R>', str(r))
    .replace('<OPACITY>', str(opacity))
    .replace('<FILL_COLOR>', str(fillColor))
    for p in circleTempStr ]

# ------------------------------------------------------------------------------
# @brief      Acts as parser core. Creates buffers containing XML tag payload.
# @param      infile   The svg file whose nodes are to be marked.
# @return     mPaths:   Holds all node coordinates of a defined svg path. offs:
#             Returns transformation/translation coordinates if corresponding
#             tags wherefound, else (0, 0)
#
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
            m = re.findall('translate\(([-+]?[0-9\.]+)\,([-+]?[0-9\.]+)\)',
                g.getAttribute('transform'), re.DOTALL)
            offs = [ float(m[0][0]), float(m[0][1]) ]
    print("No xml-tag <g> found!")

    # Get all path attributes and the paths identifier
    rawPathsIds = [ (path.getAttribute('d'),
        path.getAttribute('id')) for path in svg_dom.getElementsByTagName('path') ]
    # Create Path() class instance
    mPaths = []
    [ mPaths.append( Paths(s[1], parse_path(s[0]), offs) ) for s in rawPathsIds ]

    invEl = []
    # Check for invalid path elements and remove them
    # for k in range(len(mPaths)):
    #   if not mPaths[k].isValid():
    #       invEl.append(k)

    [ invEl.append(k) if not mPaths[k].isValid() else '' for k in range(len(mPaths)) ]
    # print("lbefore: %i  len(mPaths): %i" % (lbefore, len(mPaths)))
    print("invEl: ", invEl)
    for k in invEl:
        del mPaths[k]

    return (mPaths, offs)

# ------------------------------------------------------------------------------
# @brief      Manipulate path attributes in xml source tree.
# @param      infile    The svg input file.
# @param      valPair   Value-pair which should be modified
# @param      suffix    Optional output file suffix
# @return     Outfile pathe/name.
#
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

# ------------------------------------------------------------------------------
# @brief      Places a node marker on each node.
# @param      infile       The svg file whose nodes are to be marked.
# @param      mPaths        Paths class instance.
# @param      MARKER_SIZE   Size of node markers [px].
# @return     -
#
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

# ------------------------------------------------------------------------------
# @brief      Input argument parser.
# @param      argv   List of input arguments.
# @return     Input file path, doPretty flag.
#
def main(argv):
    flags = { 'logfile': False, 'incfile': False, 'strokes': False, 'marker': False, 'pretty': False }

    infile = None
    outs = {'logfile':'', 'incfile':''}

    cmdUsage = '%s -i <infile> [-p]' % os.path.basename(__file__)


    try:
        onodes, args = getopt.getopt(argv,"hi:smpl:c:",
            ["ifile=", "strokes", "marker", "pretty", "logfile=", "incfile="])
    except getopt.GetoptError:
        print(cmdUsage, getopt.GetoptError)
        sys.exit(2)

    for opt, arg in onodes:
        if opt == '-h':
            print(cmdUsage)
            sys.exit()
        elif opt in ("-i", "--ifile"):      infile = arg
        elif opt in ("-l", "--logfile"):    flags['logfile'] = True; outs['logfile'] = arg
        elif opt in ("-c", "--incfile"):flags['incfile'] = True; outs['incfile'] = arg
        elif opt in ("-s", "--strokes"):    flags['strokes'] = True
        elif opt in ("-m", "--marker"):     flags['marker'] = True
        elif opt in ("-p", "--pretty"):     flags['pretty'] = True

    if not os.path.isfile(infile):
        print('Input file "%s" not valied!' % infile)

    return (infile, outs, flags)

# ------------------------------------------------------------------------------
# Script run.


if __name__ == "__main__":
    mPaths = []
    dprint('sys.argv: ', sys.argv)

    try:
        (infile, outs, flags) = main(sys.argv[1:])      # Parse input arguments
        logfile = outs['logfile']
        incfile = outs['incfile']
    except:
        print("Exception while getopts!")
        osd.crit("Exception while getopts!").send()

    try:
        (mPaths, offs) = doParse(infile)            # Get paths from vector graphic
    except:
        if not mPaths:
            print("Error, no paths or bad -i argument")
        exit()

    for p in mPaths:
        dprint(p.getLines())

    if offs:
        print("offs attr: %f, %f" % (offs[0], offs[1]))

    ofile = infile
    suff = '_mod'
    # Manipulate path style attributes
    if flags['strokes']:
        ofile = styleManipulate(infile, 'stroke-opacity:0.3', suff)
        suff = ''

    # Place node markers into xml-tree of selected infile.
    if flags['marker']:
        placeNodeMarker(ofile, mPaths, 2, suff)

# , MATLAB_PRJ + os.path.basename(infile) + '.log'
    printPretty = PrettyPrint(mPaths)
    logCreate = CreateLog(mPaths, logfile=logfile)
    includeCreate = CreateInclude(mPaths, incfile=incfile)

    # Pretty print(nodes to console.)
    if flags['pretty']:
        printPretty.out(numberLines=True)
    if flags['logfile']:
        logCreate.out()
    if flags['incfile']:
        includeCreate.out()

    lin = []
    [lin.append(len(path.getLines())) for path in mPaths]
    print("Paths count: %i" % len(mPaths))
    print("Lines count: %i" % sum(lin))
    print("Nodes count: %i" % (sum(lin) + len(mPaths)))

    osd.warn('Lumpy??').send()
    lumpy.object_diagram()
    lumpy.class_diagram()
    osd.warn('Lumpy done ').send()

    # print("logfile: %s" % logfile)
    # print('len(logData): %i' % len(logData), logData)
    # osd.osdwarn(MATLAB_PRJ + os.path.basename(
    # infile).splitext()[0] + '.log',msgTitle='log write',tSec=10)

########################################
#   Script end.
########################################
