
def getAllSlots(cls):
	slots = []
	for superclass in cls.__bases__:
		slots += getAllSlots(superclass)
	
	if hasattr(cls, '__slots__'):
		slots += cls.__slots__
	
	return slots
		
#############################################################
# Basic Nodes
#############################################################

class IRNode(object):
	def __init__(self, *args, **kwparams):
		if args != ():
			slots = self.slots()
			assert len(slots) == len(args),	\
				"wrong components %s to %s's %s" % (args, self.name(), slots)
			vals = zip(slots, args)
		else:
			vals = kwparams.items()
		
		for (key, val) in vals:
			setattr(self, key, val)
	
	isa = isinstance
	
	def slots(self):
		return getAllSlots(self.__class__)
	
	def contents(self):
		return [
			(slot, getattr(self, slot))
			for slot in self.slots()
			if hasattr(self, slot)
		]
	
	def name(self):
		return self.__class__.__name__

	def __repr__(self):
		attrs = ['%s = %s' % attr for attr in self.contents()]
		attrsRep = ', '.join(attrs)
		nodename = self.name()
		if attrsRep == '': return nodename
		return '<%s of %s>' % (nodename, attrsRep)

import utils

class _IRVar(IRNode):
	value = None
	# use if there's some kind of constant value, like a class, function, or potentially literal
	
	unifiedVar = None
	# if univiedVar is not none, use this as a proxy for it

	__slots__ = ['num', 'name', 'value', 'unifiedVar'] 
	# and some type stuff...
	
	def __init__(self, nameSuggestion=''):
		self.num = utils.nextUniqueNum
		self.name = utils.uniqueID(nameSuggestion)
		self.unifiedVar = self
	
	def __eq__(lhs, rhs):
		return lhs.num == rhs.num
	
	def isActually(lhs, rhs):
		lhs.num = rhs.num
		lhs.name = rhs.name
		lhs.unifiedVar = rhs.unifiedVar
		#probably something with values/types but that's beyond here
	
	def __repr__(self):
		return self.name

