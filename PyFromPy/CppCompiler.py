
from os import system, path
import platform

compilerroot = path.dirname(path.dirname(__file__))
if platform.mac_ver()[0] != '':	#is MacOS
	pyheaders = '/System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/'
else:
	pyheaders = '/usr/include/python2.7'

def build(cppfile, exefile, print_command=False, warn=False, debug_symbols=False):
	command = ' '.join([
		'g++',

		'-g' if debug_symbols else '',
		'-Wall' if warn else '',

		'-I %s' % pyheaders,
		'-I %s/pylib' % compilerroot,
		'-L%s/pylib' % compilerroot,

		 cppfile,

		 '-lP3',
		 '-lpython2.7',
		 '-O3',
		 '-o %s' % exefile
	])

	if print_command: print command
	system(command)
