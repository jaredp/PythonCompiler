
def escapeString(s):
	escape_sequences = {
		'\\': '\\\\',
		'\n': '\\n',
		'\t': '\\t'
	}

	for (c, es) in escape_sequences.items():
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
