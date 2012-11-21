
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
			vals = zip(self.slots(), args) + kwparams.items()
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
	
	def __repr__(self):
		classname = self.__class__.__name__
		attrs = ['%s = %s' % attr for attr in self.contents()]
		attrsRep = ', '.join(attrs)
		return '<%s of %s>' % (classname, attrsRep)

import utils

class IRVar(IRNode):
	value = None
	# use if there's some kind of constant value, like a class, function, or potentially literal
	
	unifiedVar = None
	# if univiedVar is not none, use this as a proxy for it

	__slots__ = ['num', 'name', 'value', 'unifiedVar'] 
	# and some type stuff...
	
	def __init__(self, nameSuggestion=''):
		self.num = utils.nextUniqueNum
		self.name = utils.uniqueID(nameSuggestion)
	
	def __eq__(lhs, rhs):
		return lhs.num == rhs.num
	
	def isActually(lhs, rhs):
		lhs.num = rhs.num
		lhs.name = rhs.name
		lhs.unifiedVar = rhs
		#probably something with values/types but that's beyond here
	
	def __repr__(self):
		return self.name

