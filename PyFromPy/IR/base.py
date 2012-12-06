from utils import getAllSlots

#############################################################
# Basic Nodes
#############################################################

class IRNode(object):
	def __init__(self, *args, **kwargs):
		slots = self.slots()
		components = zip(slots, args) + kwargs.items()
		self.init(components)

	def init(self, components):
		for (key, val) in components:
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
		nodename = self.name()

		contents = self.contents()
		if contents == []:
			return nodename

		if contents[0][0] == 'target':
			target = repr(contents[0][1]) + ' = '
			contents = contents[1:]
		else:
			target = ''

		attrs = ', '.join(['%s = %s' % attr for attr in contents])
		if attrs != '':
			return '%s<%s of %s>' % (target, nodename, attrs)
		else:
			return '%s<%s>' % (target, nodename)

import utils

class IRVar(object):
	# use value if there's some kind of constant value, like a class, function, or potentially literal
	# if univiedVar is not none, use this as a proxy for it
	def getUnifiedVar(self):
		return self.unifiedVar.getUnifiedVar() if self.unifiedVar else self

	__slots__ = ['num', 'name', 'value', 'unifiedVar'] 
	# and some type stuff...
	
	def __init__(self, nameSuggestion=''):
		self.num = utils.nextUniqueNum
		self.name = utils.uniqueID(nameSuggestion)
		self.unifiedVar = None
		self.value = None
	
	def __eq__(lhs, rhs):
		return lhs.getUnifiedVar().num == rhs.getUnifiedVar().num
	
	def isActually(lhs, rhs):
		lhs.unifiedVar = rhs
		#probably something with values/types but that's beyond here
	
	def __repr__(self):
		return self.getUnifiedVar().name

