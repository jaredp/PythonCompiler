from IR import *
from contextlib import contextmanager

activeBlockStack = []
def enterBlock(block):	activeBlockStack.append(block)
def leaveBlock():		activeBlockStack.pop()
def currentBlock():		return activeBlockStack[-1]
def emit(op):			
	assert isinstance(op, IRNode), "tried to emit %s" % s
	currentBlock().append(op)

@contextmanager
def IRBlock(block):
	assert isinstance(block, list), "tried to enter %s" % block

	enterBlock(block)
	yield
	leaveBlock()


def emitting_new(cls, *args, **kwargs):
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
	self.init(components)

	if noemit == False:
		emit(self)
	
	return ret


@contextmanager
def autoemit():
	oldnew = IRNode.__new__
	oldinit = IRNode.__init__

	IRNode.__new__ = staticmethod(emitting_new)
	IRNode.__init__ = object.__init__

	yield
	IRNode.__new__ = oldnew
	IRNode.__init__ = oldinit