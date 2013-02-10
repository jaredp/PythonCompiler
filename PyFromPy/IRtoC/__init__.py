from CTranslator import setup, generateProgram

def translateProgram(program, out):
	setup(out)
	generateProgram(program)
	out.flush()
	
	