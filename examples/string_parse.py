def parse(s, fmt):
	separators = fmt.split('%s')
	captures = []

	captureFirst = separators[0] == ''
	captureLast = separators[-1] == ''

	separators = separators[
		1 if captureFirst else 0 :
		-1 if captureLast else None
	]

	remaining = s
	for separator in separators:
		cap, sep, remaining = remaining.partition(separator)
		if sep != separator:
			raise Exception("'%s' doesn't match '%s' on '%s'" % (s, fmt, separator))
		captures.append(cap)

	if not captureFirst and captures.pop(0) != '': raise
	if captureLast: captures.append(s)

	return captures

print parse('Jared Pochtar (jrp2181)', '%s (%s)')
