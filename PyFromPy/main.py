#!/usr/bin/python

import AstTranslator
import Optimizer
import IRtoC

from os import system, path
import platform

command_line_flags = {}

def _main(mainfile):
	program = AstTranslator.translateFile(mainfile)
	Optimizer.correct(program)

	if '-i' in command_line_flags:
		program.pprint()
		return

	pname = mainfile.rpartition('.')[0]
	cppfile = pname + '.cpp'

	IRtoC.generateProgram(program, open(cppfile, 'w'))

	gcc(cppfile, pname)

compilerroot = path.dirname(path.dirname(__file__))
pylibflag = '-lpython2.7'
if platform.mac_ver()[0] != '':	#is MacOS
	pyheaders = '/System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/'
else:
	pyheaders = '/usr/include/python2.7'

def gcc(cppfile, exefile):
	command = ' '.join([
		'g++',
		'-I %s' % pyheaders,
		'-I %s/pylib' % compilerroot,

		 '%s/pylib/P3Lib.o' % compilerroot,
		 cppfile,

		 pylibflag,

		 '-o %s' % exefile
	])

	print command
	system(command)

# http://code.activestate.com/recipes/52215/
import sys, traceback

def errlog(obj):
	print >>sys.stderr, obj

def print_exc_plus():
	"""
	Print the usual traceback information, followed by a listing of all the
	local variables in each frame.
	"""
	tb = sys.exc_info()[2]
	while 1:
		if not tb.tb_next:
			break
		tb = tb.tb_next
	stack = []
	f = tb.tb_frame
	while f:
		stack.append(f)
		f = f.f_back
	stack.reverse()
	traceback.print_exc()
	errlog("Locals by frame, innermost last")
	for frame in stack:
		errlog('')
		errlog("Frame %s in %s at line %s" %
			   (frame.f_code.co_name,
				frame.f_code.co_filename,
				frame.f_lineno)
			   )
		for key, value in frame.f_locals.items():
			#We have to be careful not to cause a new error in our error
			#printer! Calling str() on an unknown object could cause an
			#error we don't want.
			try:
				errlog("\t%20s = %s" % (key, value))
			except:
				errlog("\t%20s = <ERROR WHILE PRINTING VALUE>" % key)


def parseFlags(flags):
	command_line_flags['files'] = []
	currentflag = command_line_flags['files']

	for flag in flags:
		if flag.startswith('-'):
			command_line_flags[flag] = []
			currentflag = command_line_flags[flag]
		else:
			currentflag.append(flag)

def main():
	try:
		parseFlags(sys.argv[1:])
		files = command_line_flags['files']
		if len(files) != 1:
			print 'usage: py++ file -flags'
			exit()
		mainfile = files[0]
		
		try:
			_main(mainfile)
		except AstTranslator.UserProgramError as e:
			if '-ce' in command_line_flags: raise
			else: print e
	except:
		if '-t' in command_line_flags: print_exc_plus()
		else: raise

if __name__ == '__main__':
	main()
	
