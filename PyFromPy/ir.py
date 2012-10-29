class IRNode(object):
	pass

def makeSubclass(superclass, name, components):
	globals()[name] = type(name, (superclass,), {'__slots__':components})

[makeSubclass(IRAtom, newnode, components) for (newnode, components) in {
	
}.items()]

[makeSubclass(IRNode, newnode, components) for (newnode, components) in {
	'IRAtom': ['name'],
	'IROperation': ['target']
}.items()]

[makeSubclass(IRAtom, newnode, components) for (newnode, components) in {
	'IRVar': 
}.items()]

[makeSubclass(IRAtom, newnode, components) for (newnode, components) in {

}.items()]

[makeSubclass(IRAtom, newnode, components) for (newnode, components) in {

}.items()]
