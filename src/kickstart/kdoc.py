#! @PYTHON@
#
# $Id: kdoc.py,v 1.13 2010/09/07 23:53:07 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: kdoc.py,v $
# Revision 1.13  2010/09/07 23:53:07  bruno
# star power for gb
#
# Revision 1.12  2009/05/01 19:07:07  mjk
# chimi con queso
#
# Revision 1.11  2008/10/18 00:56:01  mjk
# copyright 5.1
#
# Revision 1.10  2008/03/06 23:41:43  mjk
# copyright storm on
#
# Revision 1.9  2007/06/23 04:03:23  mjk
# mars hill copyright
#
# Revision 1.8  2006/09/11 22:47:16  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:37  mjk
# 4.2 copyright
#
# Revision 1.6  2006/01/16 06:48:58  mjk
# fix python path for source built foundation python
#
# Revision 1.5  2005/10/12 18:08:39  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:02:19  mjk
# updated copyright
#
# Revision 1.3  2005/07/11 23:51:35  mjk
# use rocks version of python
#
# Revision 1.2  2005/05/24 21:21:54  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/01 02:02:48  mjk
# moved from core to base
#
# Revision 1.4  2004/04/14 00:33:36  fds
# Added generated by kdoc line to sgml output
#
# Revision 1.3  2004/04/09 15:17:12  fds
# For usersguide. Updated kdoc requires new rocks.util (from pylib).
#
# Revision 1.2  2004/03/25 03:15:41  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.1  2003/09/11 16:50:10  mjk
# - globus screen can run standalone
# - added kdoc.py
# - added nodes.sgml (generated from kdoc.py)
# - changed appendix a in docs
# - added appendix b (node docs) to usersguide
#

import os
import sys
import string
import xml
import popen2
import rocks.app
import rocks.util
import rocks.graph
from xml.sax import saxutils
from xml.sax import handler
from xml.sax import make_parser


class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)
		self.usage_name		= 'Kickstart Document Generator'
		self.usage_version	= '@VERSION@'
		self.graph		= 'default'
		self.xmlNodes           = []
		self.donthave = []

		# Add application flags to inherited flags

		self.getopt.s.extend([
			('g:', 'graph')
			])
		self.getopt.l.extend([
			('graph=', 'graph'),
			])

	def usageTail(self):
		return ' [file]'

	def parseArg(self, c):
		if rocks.sql.Application.parseArg(self, c):
			return 1
		elif c[0] in ('-g', '--graph'):
			self.graph = c[1]
		else:
			return 0
		return 1

	def parseNode(self, node):
		
		nodesPath = [ os.path.join('.',  'nodes'),
			      os.path.join('.',  'site-nodes') ]


		# Find the xml file for each node in the graph.  If we
		# can't find one just complain and abort.

		xml = [ None, None, None ] # rocks, extend, replace
		for dir in nodesPath:
			if not xml[0]:
				file = os.path.join(dir, '%s.xml' % node.name)
				if os.path.isfile(file):
					xml[0] = file
			if not xml[1]:
				file = os.path.join(dir, 'extend-%s.xml'\
						    % node.name)
				if os.path.isfile(file):
					xml[1] = file
			if not xml[2]:
				file = os.path.join(dir, 'replace-%s.xml'\
						    % node.name)
				if os.path.isfile(file):
					xml[2] = file

		if not (xml[0] or xml[2]):
			sys.stderr.write('error - cannot find node "%s"\n' \
				% node.name)
			self.donthave.append(node.name)
			return

		xmlFiles = [ xml[0] ]
		if xml[1]:
			xmlFiles.append(xml[1])
		if xml[2]:
			xmlFiles = [ xml[2] ]

		for xmlFile in xmlFiles:
			fin = open(xmlFile, 'r')
			parser = make_parser()
			handler = NodeHandler(node, xmlFile)
			parser.setContentHandler(handler)
			parser.parse(fin)
			fin.close()

		return handler


	def document(self, node, description, parents, children):
		print
		print '<section id="s-%s" xreflabel="%s">' % (node, node)
		print '<title>%s</title>' % node
		print '<para>'
		print description
		print '</para>'

		if parents:
			print '<para>'
			print '<emphasis>Parent Nodes:</emphasis>'
			print   '<itemizedlist>'
			for p in parents:
				link = '<xref linkend="s-%s">' % p
				if p in self.donthave:
					link = p
				print '<listitem><para>%s</para></listitem>' % link
			print   '</itemizedlist>'
			print '</para>'

		if children:
			print '<para>'
			print '<emphasis>Children Nodes:</emphasis>'
			print   '<itemizedlist>'
			for c in children:
				link = '<xref linkend="s-%s">' % c
				if c in self.donthave:
					link = c
				print '<listitem><para>%s</para></listitem>' % link
			print   '</itemizedlist>'
			print '</para>'

		print '</section>'

		
	def header(self):
		print '<!-- Generated by kdoc.py. Do not edit -->'
		print '<section id="base-nodes" xreflabel="Rocks Base Nodes">'
		print '<title>Rocks Base Nodes</title>'

	def footer(self):
		print '</section>'

	def run(self):
		parser  = make_parser()
		handler = GraphHandler()

		if not os.path.exists('graphs'):
			err = 'error - cannot find graphs dir. Runme in a build env.\n'
			sys.stderr.write(err)
			sys.exit(1)

		self.header()

		graph_dir = os.path.join('graphs', self.graph)

		for file in os.listdir(graph_dir):
			root, ext = os.path.splitext(file)
			if ext == '.xml':
				path = os.path.join(graph_dir, file)
				if os.path.isfile(path):
					fin = open(path, 'r')
					parser.setContentHandler(handler)
					parser.parse(fin)
					fin.close()

                g = handler.getGraph()

		list = []
		for node in g.getNodes():
			list.append((node.name, node))
		list.sort()

		for name,node in list:
			children = []
			parents  = []

			for e in g[node]:
				children.append(e.getChild().name)
			children.sort()

			g.reverse()
			for e in g[node]:
				parents.append(e.getChild().name)
			g.reverse()
			parents.sort()

			handler = self.parseNode(node)
			if not handler:
				continue

			self.document(name,
				      handler.description,
				      parents,
				      children)

		self.footer()


	
class GraphHandler(rocks.util.ParseXML):

	def __init__(self):
		rocks.util.ParseXML.__init__(self)
		self.graph		= rocks.graph.Graph()
		self.attrs		= rocks.util.Struct()
		self.attrs.default	= rocks.util.Struct()


	def getGraph(self):
		return self.graph


	def addEdge(self):
		if self.graph.hasNode(self.attrs.parent):
			head = self.graph.getNode(self.attrs.parent)
		else:
			head = Node(self.attrs.parent)

		if self.graph.hasNode(self.attrs.child):
			tail = self.graph.getNode(self.attrs.child)
		else:
			tail = Node(self.attrs.child)

		e = Edge(tail, head)
		e.setArchitecture(self.attrs.arch)
		e.setRelease(self.attrs.release)
		self.graph.addEdge(e)



	# <to>

	def startElement_to(self, name, attrs):	
		self.text		= ''
		self.attrs.arch		= self.attrs.default.arch
		self.attrs.release	= self.attrs.default.release

		if attrs.has_key('arch'):
			self.attrs.arch = attrs['arch']
		if attrs.has_key('release'):
			self.attrs.release = attrs['release']

	def endElement_to(self, name):
		self.attrs.parent = self.text
		self.addEdge()	
		self.attrs.parent = None
	

	# <from>

	def startElement_from(self, name, attrs):
		self.text		= ''
		self.attrs.arch		= self.attrs.default.arch
		self.attrs.release	= self.attrs.default.release
		
		if attrs.has_key('arch'):
			self.attrs.arch = attrs['arch']
		if attrs.has_key('release'):
			self.attrs.release = attrs['release']


	def endElement_from(self, name):
		self.attrs.child = self.text
		self.addEdge()
		self.attrs.child = None
		

	# <edge>
	
	def startElement_edge(self, name, attrs):
		if attrs.has_key('arch'):
			self.attrs.default.arch = attrs['arch']
		else:
			self.attrs.default.arch = None
		if attrs.has_key('release'):
			self.attrs.default.release = attrs['release']
		else:
			self.attrs.default.release	= None
		if attrs.has_key('to'):
			self.attrs.parent = attrs['to']
		else:
			self.attrs.parent = None
		if attrs.has_key('from'):
			self.attrs.child = attrs['from']
		else:
			self.attrs.child = None


	def endElement_edge(self, name):
		if self.attrs.parent and self.attrs.child:
			self.addEdge()


	def endDocument(self):
		pass



class NodeHandler(rocks.util.ParseXML):

	def __init__(self, node, filename):
		rocks.util.ParseXML.__init__(self)
		self.filename    = filename
		self.node        = node
		self.description = ''

	# <kickstart>
	
	def startElement_kickstart(self, name, attrs):
		pass
	
	def endElement_kickstart(self, name):
		pass


	# <description>

	def startElement_description(self, name, attrs):
        	self.text = ''


	def endElement_description(self, name):
        	self.description = self.text

				
				
class Node(rocks.graph.Node):

	def __init__(self, name):
		rocks.graph.Node.__init__(self, name)
		self.xmlText       = ''
		self.xmlMethods    = []
		self.xmlAttributes = []

	def addAttribute(self, attr):
		if attr not in self.xmlAttributes:
			self.xmlAttributes.append(attr)

	def addMethod(self, method):
		if method not in self.xmlMethods:
			self.xmlMethods.append(method)

	def addXML(self, xmlText):
		self.xmlText = self.xmlText + xmlText
		
	def getAttributes(self):
		return self.xmlAttributes

	def getMethods(self):
		return self.xmlMethods

	def getXML(self):
		return self.xmlText
		


class Edge(rocks.graph.Edge):
	def __init__(self, a, b):
		rocks.graph.Edge.__init__(self, a, b)
		self.arch    = None
		self.release = None

	def setArchitecture(self, arch):
		if arch:
			self.arch = arch

	def getArchitecture(self):
		return self.arch

	def setRelease(self, release):
		if release:
			self.release = release

	def getRelease(self):
		return self.release



app = App(sys.argv)
app.parseArgs()
app.run()

