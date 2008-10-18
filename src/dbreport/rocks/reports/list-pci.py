#! /opt/rocks/bin/python
#
# $Id: list-pci.py,v 1.13 2008/10/18 00:55:59 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# $Log: list-pci.py,v $
# Revision 1.13  2008/10/18 00:55:59  mjk
# copyright 5.1
#
# Revision 1.12  2008/03/06 23:41:41  mjk
# copyright storm on
#
# Revision 1.11  2007/06/23 04:03:21  mjk
# mars hill copyright
#
# Revision 1.10  2006/09/11 22:47:08  mjk
# monkey face copyright
#
# Revision 1.9  2006/08/10 00:09:30  mjk
# 4.2 copyright
#
# Revision 1.8  2006/01/16 06:48:57  mjk
# fix python path for source built foundation python
#
# Revision 1.7  2005/10/12 18:08:37  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:02:16  mjk
# updated copyright
#
# Revision 1.5  2005/09/15 22:45:09  mjk
# - copyright updated, but not the final notice for 4.1 (ignore this change)
# - resolv.conf now uses "search" domains for private, then public
# - resolv.conf no longer uses "domain" (replaced by "search")
# - named.conf is now created from dbreport (includes rocks.zone)
# - dns.py requires an argument ("zone", or "reverse")
# - dns config removed (now in named)
# - general dns.py cleanup (simpler logic, tossed dead code)
# - removed domain name related functions from base.py
# - added getGlobalVar to base.py (don't have to go through self.sql anymore)
# - did a diff of the reports vs existing files on rocks-153, looks good
#
# Revision 1.4  2005/07/11 23:51:34  mjk
# use rocks version of python
#
# Revision 1.3  2005/05/24 21:21:52  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2005/05/23 23:59:22  fds
# Frontend Restore
#
# Revision 1.1  2005/03/01 02:02:46  mjk
# moved from core to base
#
# Revision 1.3  2004/03/25 03:15:35  bruno
# touch 'em all!
#
# update version numbers to 3.2.0 and update copyrights
#
# Revision 1.2  2003/09/30 22:39:19  fds
# Version field is hex
#
# Revision 1.1  2003/09/30 22:23:27  fds
# Reports that query the database for various PCI information about cluster nodes.
#


import rocks.reports.base


class Report(rocks.reports.base.ReportBase):

	def run(self):

		if not self.connect():
			print "Could not connect to db!"
			return

		if len(self.args):
			# Show pcis for one node.
			node = self.args[0]
			nodeid = self.sql.getNodeId(node)
			query="select class, vendor, device, version from \
				pcis p, nodes_pcis n where n.node=%d \
				and n.pci = p.id" % nodeid

			self.execute(query)
			if self.rowcount():
				print "PCI devices for node", node
				print "Class: Vendor:Device (Version)"
				for row in self.fetchall():
					print "Class %s: %s:%s (rev %02x)" % (row)

		else:
			# Show all pcis for all nodes.
			self.execute("select n.id, name, class, vendor, "
				"device, version from nodes n, pcis p, "
				"nodes_pcis np where n.site=0 and "
				"n.id = np.node and p.id = np.pci")
			if self.rowcount():
				print "PCI devices for all nodes"
				print "id Name: Class: Vendor:Device (Version)"
				for row in self.fetchall():
					print "%d %s: Class %s: %s:%s (rev %02x)" % (row)
					
