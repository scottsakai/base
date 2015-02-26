#autogenerated by sqlautocode

import sqlalchemy.ext.declarative
import sqlalchemy.orm
from sqlalchemy import *

# generated with https://github.com/lclementi/sqlautocode
# using command line:
#  sqlautocode mysql://root:zzzzzzz@localhost/cluster -o base.py -d -g
# Then edited manually a lot


Base = sqlalchemy.ext.declarative.declarative_base()


 
class RocksBase(object):
	"""Additional base class of Rocks ORM hierarchy which includes some
	helper methods for all classes"""

	@property
	def session(self):
		"""Singelton which return the session of the object"""
		return sqlalchemy.orm.session.object_session(self)


	def delete(self):
		"""instance method to autodelete the instance which calls it

		so you can use
		node.delete()"""
		self.session.delete(self)

	@classmethod
	def loadOne(cls, session, **kwargs):
		""" """
		return cls.load(session, **kwargs).one()


	@classmethod
	def load(cls, session, **kwargs):
		"""
		this method allow us to run query on all the mapping objects
		simply using 

		e.g.::

		  node = Nodes.load(session, Name='compute-0-0', Cpus=2)
		  nic = Network.load(session, Name='compute-0-0', Interface='eth0')

		taken from:
		http://petrushev.wordpress.com/2010/06/22/sqlalchemy-base-model/
		"""
		q = session.query(cls)
		filters = [getattr(cls, field_name)==kwargs[field_name] \
				for field_name in kwargs]
		return q.filter(and_(*filters))



class Alias(RocksBase, Base):
	__tablename__ = 'aliases'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	node_ID = Column('Node', Integer, ForeignKey('nodes.ID'),
					nullable=False, default=0)
	name = Column('Name', String(32))

	# relation definitions
	# node from nodes


class Appliance(RocksBase, Base):
	__tablename__ = 'appliances'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(32), nullable=False, default='')
	graph = Column('Graph', String(64), nullable=False, default='default')
	node = Column('Node', String(64), nullable=False, default='')
	os = Column('OS', Enum(u'linux', u'sunos'), nullable=False, default=u'linux')

	#relation definitions
	memberships = sqlalchemy.orm.relationship("Membership", backref="appliance")



class ApplianceRoute(RocksBase, Base):
	__tablename__ = 'appliance_routes'

	__table_args__ = {}

	#column definitions
	appliance = Column('Appliance', Integer, primary_key=True, nullable=False)
	network = Column('Network', String(32), primary_key=True, nullable=False)
	netmask = Column('Netmask', String(32), primary_key=True, nullable=False)
	gateway = Column('Gateway', String(32), nullable=False)
	subnet = Column('Subnet', Integer, ForeignKey('subnets.ID'), nullable=True)

	#relation definitions


class Attribute(RocksBase, Base):
	__tablename__ = 'attributes'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	attr = Column('Attr', String(128), nullable=False)
	value = Column('Value', TEXT())
	shadow = Column('Shadow', TEXT())
	categoryID = Column('Category', Integer, ForeignKey('categories.ID'), nullable=False)
	catindexID = Column('Catindex', Integer, ForeignKey('catindex.ID'), nullable=False)

	#relation definitions


class Boot(RocksBase, Base):
	__tablename__ = 'boot'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	node_ID = Column('Node', Integer, ForeignKey('nodes.ID'), nullable=False, default=0)
	action = Column('Action', Enum(u'install', u'os', u'run'))

	#relation definitions
	node = sqlalchemy.orm.relationship("Node", 
		backref=sqlalchemy.orm.backref("boot", uselist=False))


class Bootaction(RocksBase, Base):
	__tablename__ = 'bootaction'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	action = Column('Action', String(256))
	kernel = Column('Kernel', String(256))
	ramdisk = Column('Ramdisk', String(256))
	args = Column('Args', String(1024))

	#relation definitions


class Bootflag(RocksBase, Base):
	__tablename__ = 'bootflags'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	flags = Column('Flags', String(256))
	node = Column('Node', Integer, nullable=False)

	#relation definitions


class Category(RocksBase, Base):
	__tablename__ = 'categories'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(64), nullable=False)
	description = Column('Description', String(512))

	#relation definitions
	attributes = sqlalchemy.orm.relationship("Attribute", backref="category")
	catindexes = sqlalchemy.orm.relationship("Catindex", backref="category")


class Catindex(RocksBase, Base):
	__tablename__ = 'catindex'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(64), nullable=False)
	categoryID = Column('Category', Integer, ForeignKey('categories.ID'), nullable=False)

	#relation definitions
	attributes = sqlalchemy.orm.relationship("Attribute", backref="catindex")


class Distribution(RocksBase, Base):
	__tablename__ = 'distributions'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	lang = Column('Lang', String(32), nullable=False, default='')
	name = Column('Name', String(32), nullable=False, default='')
	os_Release = Column('OS_Release', String(32), nullable=False, default='')

	#relation definitions


class Firewall(RocksBase, Base):
	__tablename__ = 'firewalls'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	rulename = Column('Rulename', String(128), nullable=False)
	rulesrc = Column('Rulesrc', Enum(u'system', u'custom'), nullable=False, default=u'custom')
	inSubnet = Column('InSubnet', Integer)
	outSubnet = Column('OutSubnet', Integer)
	service = Column('Service', String(256))
	protocol = Column('Protocol', String(256))
	action = Column('Action', String(256))
	chain = Column('Chain', String(256))
	flags = Column('Flags', String(256))
	comment = Column('Comment', String(256))
	category = Column('Category', Integer, nullable=False)
	catindex = Column('Catindex', Integer, ForeignKey('catindex.ID'), nullable=False)

	#relation definitions


class GlobalRoute(RocksBase, Base):
	__tablename__ = 'global_routes'

	__table_args__ = {}

	#column definitions
	gateway = Column('Gateway', String(32), nullable=False)
	netmask = Column('Netmask', String(32), primary_key=True, nullable=False)
	network = Column('Network', String(32), primary_key=True, nullable=False)
	subnet = Column('Subnet', Integer, ForeignKey('subnets.ID'))

	#relation definitions



class Membership(RocksBase, Base):
	__tablename__ = 'memberships'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(64), nullable=False)
	appliance_ID = Column('Appliance', Integer, ForeignKey('appliances.ID'), default=0)
	distribution_ID = Column('Distribution', Integer, ForeignKey('distributions.ID'), default=1)
	public = Column('Public', Enum(u'yes', u'no'), nullable=False, default=u'no')

	#relation definitions
	nodes = sqlalchemy.orm.relationship("Node", backref="membership")


class Network(RocksBase, Base):
	__tablename__ = 'networks'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	node_ID = Column('Node', Integer, ForeignKey('nodes.ID'))
	mac = Column('MAC', String(64))
	ip = Column('IP', String(32))
	name = Column('Name', String(128))
	device = Column('Device', String(32))
	subnet_ID = Column('Subnet', Integer, ForeignKey('subnets.ID'))
	module = Column('Module', String(128))
	vlanID = Column('VlanID', Integer)
	options = Column('Options', String(128))
	channel = Column('Channel', String(128))
	disable_kvm = Column('Disable_KVM', Boolean, default=False)

	# relation definitions
	# node	from nodes
	# subnet  from subnets



class Node(RocksBase, Base):
	__tablename__ = 'nodes'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(128))
	membership_ID = Column('Membership', Integer, ForeignKey('memberships.ID'), default=2)
	cpus = Column('CPUs', Integer, nullable=False, default=1)
	rack = Column('Rack', Integer)
	rank = Column('Rank', Integer)
	arch = Column('Arch', String(32))
	os = Column('OS', Enum(u'linux', u'sunos'), nullable=False, default=u'linux')
	runaction = Column('RunAction', String(64), default='os')
	installaction = Column('InstallAction', String(64), default='install')

	#relation definitions
	# map the networks belonging to this node
	networks = sqlalchemy.orm.relationship("Network", backref="node")
	public_keys = sqlalchemy.orm.relationship("PublicKey", backref="node")
	aliases = sqlalchemy.orm.relationship("Alias", backref="node")
	# backrefs defined in other tables
	# membership from memeberships
	# vm_defs	from vm_nodes
	# boot	   from boot


	def __repr__(self):
		return "<Node(name='%s')>" % (self.name)


class NodeRoll(RocksBase, Base):
	__tablename__ = 'node_rolls'

	__table_args__ = {}

	#column definitions
	node = Column('Node', Integer, primary_key=True, nullable=False)
	rollID = Column('RollID', Integer, primary_key=True, nullable=False)

	#relation definitions


class NodeRoute(RocksBase, Base):
	__tablename__ = 'node_routes'

	__table_args__ = {}

	#column definitions
	gateway = Column('Gateway', String(32), nullable=False)
	netmask = Column('Netmask', String(32), primary_key=True, nullable=False)
	network = Column('Network', String(32), primary_key=True, nullable=False)
	node = Column('Node', Integer, primary_key=True, nullable=False)
	subnet = Column('Subnet', Integer, ForeignKey('subnets.ID'))

	#relation definitions


class OsRoute(RocksBase, Base):
	__tablename__ = 'os_routes'

	__table_args__ = {}

	#column definitions
	gateway = Column('Gateway', String(32), nullable=False)
	netmask = Column('Netmask', String(32), primary_key=True, nullable=False)
	network = Column('Network', String(32), primary_key=True, nullable=False)
	os = Column('OS', Enum(u'sunos', u'linux'), primary_key=True, nullable=False, default=u'linux')
	subnet = Column('Subnet', Integer, ForeignKey('subnets.ID'))

	#relation definitions


class Partition(RocksBase, Base):
	__tablename__ = 'partitions'

	__table_args__ = {}

	#column definitions
	device = Column('Device', String(128), nullable=False)
	formatFlags = Column('FormatFlags', String(128), nullable=False)
	fsType = Column('FsType', String(128), nullable=False)
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	mountpoint = Column('Mountpoint', String(128), nullable=False)
	node = Column('Node', Integer, nullable=False)
	partitionFlags = Column('PartitionFlags', String(128), nullable=False)
	partitionID = Column('PartitionID', String(128), nullable=False)
	partitionSize = Column('PartitionSize', String(128), nullable=False)
	sectorStart = Column('SectorStart', String(128), nullable=False)

	#relation definitions


class PublicKey(RocksBase, Base):
	__tablename__ = 'public_keys'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	node_ID = Column('Node', Integer, ForeignKey('nodes.ID'), nullable=False)
	public_key = Column('Public_Key', String(4096))
	description = Column('Description', String(4096))

	#relation definitions
	# backrefs defined in other tables
	# node from Node


class Resolvechain(RocksBase, Base):
	__tablename__ = 'resolvechain'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(64), nullable=False, default=0)
	category = Column('Category', Integer, ForeignKey('categories.ID'), nullable=False)
	precedence = Column('Precedence', Integer, nullable=False, default=10)

	#relation definitions


class Roll(RocksBase, Base):
	__tablename__ = 'rolls'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('Name', String(128), nullable=False)
	version = Column('Version', String(32), nullable=False)
	arch = Column('Arch', String(32), nullable=False)
	os = Column('OS', Enum(u'linux', u'sunos'), nullable=False, default=u'linux')
	enabled = Column('Enabled', Enum(u'yes', u'no'), nullable=False, default=u'yes')

	#relation definitions


class SecGlobalAttribute(RocksBase, Base):
	__tablename__ = 'sec_global_attributes'

	__table_args__ = {}

	#column definitions
	attr = Column('Attr', String(128), primary_key=True, nullable=False)
	enc = Column('Enc', String(64))
	value = Column('Value', TEXT())

	#relation definitions


class SecNodeAttribute(RocksBase, Base):
	__tablename__ = 'sec_node_attributes'

	__table_args__ = {}

	#column definitions
	attr = Column('Attr', String(128), primary_key=True, nullable=False)
	enc = Column('Enc', String(64))
	node = Column('Node', Integer, primary_key=True, nullable=False)
	value = Column('Value', TEXT())

	#relation definitions


class Subnet(RocksBase, Base):
	__tablename__ = 'subnets'

	__table_args__ = {}

	#column definitions
	ID = Column('ID', Integer, primary_key=True, nullable=False)
	name = Column('name', String(32), nullable=False, unique=True)
	dnszone = Column('dnszone', String(64), nullable=False, unique=True)
	subnet = Column('subnet', String(32), nullable=False)
	netmask = Column('netmask', String(32), nullable=False)
	mtu = Column('mtu', Integer, default=1500)
	servedns = Column('servedns', Boolean, default=False)

	#relation definitions
	networks = sqlalchemy.orm.relationship("Network", backref="subnet")

