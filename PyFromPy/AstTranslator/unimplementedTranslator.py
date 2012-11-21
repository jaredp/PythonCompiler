
# for completeness

class UnimplementedTranslator:
	def _Assert(s, test, msg):
		pass
		# It's valid to just ignore these

	def _Exec(s, body, globals, locals):
		raise NotImplementedError
		# we *may* actually implement this

