from contextlib import contextmanager

def getAllSlots(cls):
	slots = []
	for superclass in cls.__bases__:
		slots += getAllSlots(superclass)
	
	if hasattr(cls, '__slots__'):
		slots += cls.__slots__
	
	return slots
		
#############################################################
# IR Building
#############################################################

activeBlockStack = []
def enterBlock(block):	activeBlockStack.append(block)
def leaveBlock():		activeBlockStack.pop()
def currentBlock():		return activeBlockStack[-1]
def emit(op):			
	assert isinstance(op, IRNode), "tried to emit %s" % s
	currentBlock().append(op)

@contextmanager
def IRBlock(block):
	enterBlock(block)
	yield
	leaveBlock()

#############################################################
# Basic Nodes
#############################################################

class IRNode(object):
	def __new__(cls, *args, **kwargs):
		self = object.__new__(cls)
		noemit = kwargs.pop('noemit', False)
		slots = self.slots()

		if 'target' in slots:
			# can't use kwargs.pop('target', None) or IRVar b/c target=None
			if 'target' in kwargs:
				self.target = kwargs.pop('target')
				ret = self
			else:
				self.target = IRVar()
				ret = self.target

			slots.remove('target')
		else:
			ret = self
		
		components = zip(slots, args) + kwargs.items()
		for (key, val) in components:
			setattr(self, key, val)

		if noemit == False:
			emit(self)
		
		return ret
		
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
		return '%s<%s of %s>' % (target, nodename, attrs)

import utils

class IRAtom(object):
	def __init__(self, value=None):
		self.value = value

class IRVar(IRAtom):
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

