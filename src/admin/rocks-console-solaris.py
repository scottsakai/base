#! @PYTHON@
#
# $Id: rocks-console-solaris.py,v 1.6 2009/05/01 19:06:50 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: rocks-console-solaris.py,v $
# Revision 1.6  2009/05/01 19:06:50  mjk
# chimi con queso
#
# Revision 1.5  2008/10/18 00:55:47  mjk
# copyright 5.1
#
# Revision 1.4  2008/03/06 23:41:32  mjk
# copyright storm on
#
# Revision 1.3  2007/06/23 04:03:19  mjk
# mars hill copyright
#
# Revision 1.2  2007/04/27 23:45:44  anoop
# Added the rocks-console-solaris command. This will be folded back into
# rocks console once more changes come into place
#
# Revision 1.1  2007/01/23 01:39:45  anoop
# Moved cluster-kickstart-solaris to the base roll admin package. Made more
# sense to put it there rather than in rocks-boot. Since others may have another
# opinion, I left the other files in the same spot.
#
# Alpha roll build pkgs along with RPMs.
# Foundation-mysql Makefile errors corrected.
# rocks-console gets its own solaris version for now. The changes are minimal and will
# be merged back to the original rocks-console.py file as soon as I've had a
# chance to test it further.
#
# Revision 1.8  2006/09/11 22:47:02  mjk
# monkey face copyright
#
# Revision 1.7  2006/08/10 00:09:25  mjk
# 4.2 copyright
#
# Revision 1.6  2006/08/09 15:41:38  anoop
# Changes to shootnode and rocks-console. These changes were necessary to
# support shooting multiple nodes in one command. The threading in shoot-node
# would cause a lot of problems because multiple threads would try to manipulate
# stderr, and all would fail but one.
#
# Also race conditions are created by the presence of threads, and so sockets need
# to be released only at the last possible moment, to avoid multiple bindings.
#
# Revision 1.5  2006/07/10 22:40:40  anoop
# Silly little bug removed.
#
# Revision 1.4  2006/07/03 22:13:11  anoop
# Rocks console can connect to multiple servers now without barfing
#
# Revision 1.3  2006/06/16 21:09:01  bruno
# make default local port for ekv to be 8000
#
# Revision 1.2  2006/06/15 23:04:51  bruno
# name the vncviewer window to the same name as the node it is connected to
#
# Revision 1.1  2006/06/15 21:28:47  bruno
# new command to get the vnc and ekv consoles on an installing node
#
#
#

import os
import sys
import rocks.app
import socket
import platform
import time
		        
class App(rocks.app.Application):

	def __init__(self, argv):
		rocks.app.Application.__init__(self, argv)	

		self.usage_name = 'Rocks Console'
		self.usage_version = '@VERSION@'

		self.nodename = ''
		self.known_hosts = '/tmp/.known_hosts'
		self.defaultport = 5901
		self.localport = 0
		self.remoteport = 0
		self.ekv = 0
		if platform.system() == "SunOS":
			self.tunnel_command = "x11vnc -q -nopw -once -display :0 -auth /tmp/root/.TTauthority -rfbport %d" % (self.defaultport)
		else:
			self.tunnel_command = "/bin/bash -c \"sleep 20\""

		porthelp = '(port number of VNC server - default = %d)' \
			% (self.defaultport)


		self.getopt.l.extend([
				'ekv',
				('port=', porthelp)
			])

		return


	def parseArg(self, c):
		rocks.app.Application.parseArg(self, c)

		key, val = c
		if key in ('--port'):
			self.localport = int(val)
		elif key in ('--ekv'):
			self.ekv = 1

		return


	def usageTail(self):
		return ' <nodename (e.g., compute-0-0)>\n'


	def ekvviewer(self):
		cmd = 'telnet localhost %d' % (self.localport)
		os.system(cmd)
		return


	def vncviewer(self):
		cmd = 'vncviewer -truecolor -encodings "copyrect" localhost:%d' \
			% (self.localport - self.defaultport + 1)
		os.system(cmd)

		return


	def createSecureTunnel(self):
		#
		# use a temporary file to store the host key. we do this
		# because a new temporary host key is created in the
		# installer and if we add this temporary host key to
		# /root/.ssh/known_hosts, then the next time the node is
		# installed, the ssh tunnel will get a 'man-in-middle' error
		# and not allow port forwarding.
		#
		self.known_hosts = "%s_%s" % (self.known_hosts,self.nodename)
		if os.path.exists(self.known_hosts):
			os.unlink(self.known_hosts)

		cmd = 'ssh -q -f -o UserKnownHostsFile=%s -o StrictHostKeyChecking=no ' % (self.known_hosts)
		cmd += '-L %d:localhost:%d ' % (self.localport, self.remoteport)
		cmd += '%s -p 2200 ' % (self.nodename)
		cmd += '\'%s\'' % (self.tunnel_command)
		self.s.close()
		print cmd
		os.system(cmd)

		return


	def run(self):
		if len(self.args) > 0:
			self.nodename = self.args[0]
		else:
			print '\n\t"nodename" was not specified\n'
			self.usage()
			sys.exit(-1)

		self.nodename = self.args[0]

		if self.ekv == 1:
			if self.localport == 0:
				self.localport = 8000
			self.remoteport = 8000
		else:
			if self.localport == 0:
				self.localport = self.defaultport
			self.remoteport = self.defaultport

		# Check ports to see which one is open. If ports are already bound
		# go to the next one to check. Whatever binds is successfully is used.
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		done = 0
		while(done == 0):
		 	try:
				self.s.bind(("localhost",self.localport))
				done = 1
			except socket.error,(errno,string):
			   if(errno == 98):
				done = 0
				self.localport = self.localport + 1
		
		#Connect to the secure tunnel and go...
		self.createSecureTunnel()

		#Wait for 5 seconds till the connection is established
		time.sleep(5)

		if self.ekv == 1:
			self.ekvviewer()
		else:
			self.vncviewer()

		return


app = App(sys.argv)
app.parseArgs()
app.run()

