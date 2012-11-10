#!/usr/bin/python

import PyFromPy
from gencpp import CppGenerator
from unparse import Unparser
import ast
import ASTToIR
import ir

import sys
from debug import print_exc_plus

def _main():
	if len(sys.argv) > 1:
		m = PyFromPy.parseFile(sys.argv[1])
	else:
		m = ast.parse(sys.stdin.read())
	
	#PyFromPy.transformModule(m)
	#CppGenerator(m)
	
	irmod = ASTToIR.translate(m)
	irmod.pprint()
	
	print
	print


def mainWithFancyExcept():
	try:
		_main()
	except:
		print_exc_plus()
		exit(1)


def main():
	print len(sys.argv)
	if len(sys.argv) == 3:
		print "yea I'm here"
		mainWithFancyExcept()
	else:
		_main()

if __name__ == '__main__':
	main()
	