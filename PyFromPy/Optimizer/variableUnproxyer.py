from optutils import *

def clean(program):
	for op in iterOperationsInProgram(program):
		for slot in op.slots():
			if hasattr(op, slot):
				val = getattr(op, slot)
				if isinstance(val, IRVar):
					setattr(op, slot, val.getUnifiedVar())
