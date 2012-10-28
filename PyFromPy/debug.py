
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
