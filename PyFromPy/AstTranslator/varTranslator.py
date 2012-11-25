
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

	def translateSlice(s, slice):
		if slice.lower:
			start = s.translateExpr(slice.lower)
		else:
			start = None
		if slice.upper:
			end = s.translateExpr(slice.upper)
		else:
			end = None
		if slice.step:
			step = s.translateExpr(slice.step)
		else:
			step = None
		return (start, end, step)

	def _Subscript(s, value, slice, ctx):
		if isinstance(slice, ast.Index):
			return Subscript(
				s.translateExpr(value),
			 	s.translateExpr(slice.value)
			 )

		elif isinstance(slice, ast.Slice):
			obj = s.translateExpr(value)
			start, end, step = s.translateSlice(slice)
			return Slice(obj, start, end, step)

		else:
			raise NotImplementedError

	def _Delete(s, targets):
		for target in targets:
			if isinstance(target, ast.Name):
				var = s.getTargetNamed(target.id)
				s.emit(DeleteVar(var))
				
			elif isinstance(target, ast.Attribute):
				irobj = s.translateExpr(target.value)
				s.emit(DeleteAttr(irobj, target.attr))
				
			elif isinstance(target, ast.Subscript):
				obj = s.translateExpr(target.value)

				if isinstance(target.slice, ast.Index):
					index = s.translateExpr(target.slice.value)
					return s.emit(DeleteSubscript(obj, index))
				
				elif isinstance(target.slice, ast.Slice):
					start, end, step = s.translateSlice(target.slice)
					return s.emit(DeleteSlice(obj, start, end, step))
		
				else:
					raise NotImplementedError
				
			elif type(target) in [ast.List, astTuple]:
				s._Del(target.elts)

	

	def _Assign(s, targets, value):
		rhstemp = s.translateExpr(value)
		return s.makeAssignment(targets, rhstemp)
		
	def _AugAssign(s, target, op, value):
		raise NotImplementedError
	
	def makeAssignment(s, asttargets, irrhs):
		unpackAsgns = []
	
		for target in asttargets:
			if isinstance(target, ast.Name):
				Assign(
					target=s.getTargetNamed(target.id), 
					rhs=irrhs
				)
				
			elif isinstance(target, ast.Attribute):
				#we're not assigning to the target, so we don't add it to locals
				AssignAttr(
					s.translateExpr(target.value),
					target.attr,
					irrhs
				)
				
			elif isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Index):
				AssignSubscript(
					s.translateExpr(target.value), 
					s.translateExpr(target.slice.value), 
					irrhs
				)
			
			elif isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Slice):
				obj = s.translateExpr(target.value)
				start, end, step = s.translateSlice(target.slice)
				AssignSlice(obj, start, end, step, irrhs)
				
			elif type(target) in [ast.List, ast.Tuple]:
				unpackAsgns.append(target.elts)

			else: raise NotImplementedError
			
		if len(unpackAsgns) > 0:
			iterator = stdlib.Iter(irrhs)
			
			if not all([len(upa) == len(unpackAsgns[0]) for upa in unpackAsgns]):
				s.runtimeError('too many/not enough values to unpack')
			
			for cAsgn in zip(*unpackAsgns):
				component = stdlib.Next(iterator)
				s.makeAssignment(cAsgn, component)


