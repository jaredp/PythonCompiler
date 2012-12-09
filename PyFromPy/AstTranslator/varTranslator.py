
from IR import *
import ast
from BaseTranslator import translatorMixin

@translatorMixin
class Names:
	def _Global(s, names):
		for name in names:
			s.declareGlobal(name)

	def _Name(s, id, ctx):
		if id == 'None':
			return NoneLiteral()
		#ctx *should* be ignorable
		return s.getVarNamed(id)

	def _Attribute(s, value, attr, ctx):
		obj = s.translateExpr(value)
		return Attr(obj, attr)

	def translateSlice(t, slice):
		if slice.lower:
			start = t(slice.lower)
		else:
			start = NoneLiteral()
		if slice.upper:
			end = t(slice.upper)
		else:
			end = NoneLiteral()
		if slice.step:
			step = t(slice.step)
		else:
			step = NoneLiteral()
		return (start, end, step)

	def _Subscript(t, value, slice, ctx):
		obj = t(value)

		if isinstance(slice, ast.Index):
			return stdlib.Subscript(obj, t(slice.value))

		elif isinstance(slice, ast.Slice):
			start, end, step = t.translateSlice(slice)
			return stdlib.Slice(obj, start, end, step)

		else:
			raise NotImplementedError

	def _Delete(s, targets):
		for target in targets:
			if isinstance(target, ast.Name):
				var = t.getTargetNamed(target.id)
				DeleteVar(var)
				
			elif isinstance(target, ast.Attribute):
				irobj = t(target.value)
				DeleteAttr(irobj, target.attr)
				
			elif isinstance(target, ast.Subscript):
				obj = t(target.value)

				if isinstance(target.slice, ast.Index):
					index = t(target.slice.value)
					return stdlib.DeleteSubscript(obj, index)
				
				elif isinstance(target.slice, ast.Slice):
					start, end, step = t.translateSlice(target.slice)
					return stdlib.DeleteSlice(obj, start, end, step)
		
				else:
					raise NotImplementedError
				
			elif type(target) in [ast.List, astTuple]:
				s._Del(target.elts)

	

	def _Assign(s, targets, value):
		rhstemp = s.translateExpr(value)
		return s.makeAssignments(targets, rhstemp)
	
	def makeAssignment(s, asttarget, irrhs):
		s.makeAssignments([asttarget], irrhs)

	def makeAssignments(t, asttargets, irrhs):
		unpackAsgns = []
	
		for target in asttargets:
			if isinstance(target, ast.Name):
				Assign(
					target=t.getTargetNamed(target.id), 
					rhs=irrhs
				)
				
			elif isinstance(target, ast.Attribute):
				#we're not assigning to the target, so we don't add it to locals
				AssignAttr(t(target.value), target.attr, irrhs)
				
			elif isinstance(target, ast.Subscript) \
			and isinstance(target.slice, ast.Index):
				stdlib.AssignSubscript(
					t(target.value),
					t(target.slice.value), 
					irrhs
				)
			
			elif isinstance(target, ast.Subscript) \
			and isinstance(target.slice, ast.Slice):
				obj = t(target.value)
				start, end, step = t.translateSlice(target.slice)
				stdlib.AssignSlice(obj, start, end, step, irrhs)
				
			elif type(target) in [ast.List, ast.Tuple]:
				unpackAsgns.append(target.elts)

			else: raise NotImplementedError
			
		if len(unpackAsgns) > 0:
			iterator = stdlib.Iter(irrhs)
			
			if not all([len(upa) == len(unpackAsgns[0]) for upa in unpackAsgns]):
				t.runtimeError('too many/not enough values to unpack')
			
			for cAsgn in zip(*unpackAsgns):
				component = stdlib.Next(iterator)
				t.makeAssignments(cAsgn, component)


