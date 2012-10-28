#!/usr/bin/python

import PyFromPy
from gencpp import CppGenerator
from unparse import Unparser
import ast

import sys
from debug import print_exc_plus

def main():
	try:
		if len(sys.argv) == 2:
			m = PyFromPy.parseFile(sys.argv[1])
		else:
			m = ast.parse(sys.stdin.read())
		
		PyFromPy.transformModule(m)
		CppGenerator(m)
		
		print
		print

	except:
		print_exc_plus()
		exit(1)


if __name__ == '__main__':
	main()
