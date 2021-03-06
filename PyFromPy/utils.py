import sys
#from unparse import Unparser

def log(obj):
	if isinstance(obj, AST):
		Unparser(obj, sys.stderr)
		print >>sys.stderr
	else:
		print >>sys.stderr, obj

def compose(f):
	def inner(g):
		def wrapper(*args, **kwargs):
			return f(g(*args, **kwargs))
		return wrapper
	return inner

def flattenList(l):
	for i in l:
		for j in i:
			yield j

def numbered(l):
	return zip(range(len(l)), l)

def escapeString(s):
	escape_sequences = [
		('\\', '\\\\'),
		('\n', '\\n'),
		('\t', '\\t')
	]

	for (c, es) in escape_sequences:
		s = s.replace(c, es)
	
	return s

#http://stackoverflow.com/a/4578605/257261
def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

#############################################################
# Unique names
#############################################################

nextUniqueNum = 0
def uniqueID(suggestion=''):
	global nextUniqueNum
	uid = suggestion+'$'+str(nextUniqueNum)
	nextUniqueNum += 1
	return uid

#############################################################
# __slots__ handling
#############################################################

def getAllSlots(cls):
	slots = []
	for superclass in cls.__bases__:
		slots += getAllSlots(superclass)
	
	if hasattr(cls, '__slots__'):
		slots += cls.__slots__
	
	return slots

#############################################################
# Pattern matching
# doesn't currently support slots
#############################################################

__, ___ = ig, igs  = object(), object()

class inverse:
	def __init__(self, pattern):
		self.pattern = pattern

class allmatching:
	def __init__(self, pattern):
		self.pattern = pattern

'''
ig				matches anything
igs				is ment to match 0+ things 
[igs]			matches any list
[n, igs]		matches a list that starts with n
[igs, n]		matches a list that ends in n
[igs, n, igs]	matches a list that contains n
inverse(n)		matches iff it's not n
allmatching(n)  matches iterable with all elements matching n
				NOTE: this one's untested!!
'''

def matches(node, pattern):
	if pattern == ig:					return True
	elif type(pattern) == inverse:
		return not matches(node, pattern.pattern)
	elif type(pattern) == allmatching:
		return all(matches(n, pattern.pattern) for n in node)
	elif type(pattern) == type:			return isinstance(node, pattern)
	elif type(node) != type(pattern):	return False

	if type(node) in [list, tuple]:
		if pattern == []:
			return node == []

		elif pattern[0] == igs and pattern[-1] == igs:
			return all(
				any(matches(e, p) for e in node)
				for p in pattern[1:-1]
			)

		elif pattern[-1] == igs:
			pattern = pattern[:-1]
			if len(pattern) > len(node): return False
			node = node[:len(pattern)]
			
		elif pattern[0] == igs:
			pattern = pattern[1:]
			if len(pattern) > len(node): return False
			node = node[-len(pattern):]
			
		return len(node) == len(pattern) and all(
			matches(n, p) for (n, p) in
			zip(node, pattern)
		)
	
	elif hasattr(node, '__dict__'):
			for k, v in pattern.__dict__.items():
				if not matches(node.__dict__[k], v):
					return False
			return True
	
	else:
		return node == pattern
			
			
			