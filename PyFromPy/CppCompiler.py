
from os import system, path
import platform

compilerroot = path.dirname(path.dirname(__file__))
pylibflag = '-lpython2.7'
if platform.mac_ver()[0] != '':	#is MacOS
	pyheaders = '/System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/'
else:
	pyheaders = '/usr/include/python2.7'

def build(cppfile, exefile):
	command = ' '.join([
		'g++',

		'-Wall',

		'-I %s' % pyheaders,
		'-I %s/pylib' % compilerroot,

		 '%s/pylib/P3Lib.o' % compilerroot,
		 cppfile,

		 pylibflag,

		 '-o %s' % exefile
	])

	system(command)
