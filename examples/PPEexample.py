from __builtin__ import globals, int, raw_input


def declare(member, value):
	attr = 'a_%s' % member
	globals()[attr] = value
	print attr, value

declare('foo', 'bar')
declare('name', 'xyz')

def print_foo():
	print a_foo

def print_name():
	print a_name

declare('p', print_foo)
declare('q', print_name)

#a_p()

if int(raw_input('')) > 5:
	a_p()
else:
	a_q()

