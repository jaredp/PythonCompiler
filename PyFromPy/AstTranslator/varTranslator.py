
from IR import *
import ast
from BaseTranslator import translatorMixin

@translatorMixin
class Names:
	def _Global(s, names):
		if s.isInGlobalBlock():
			s.error("global declaration in global scope")
		
		for name in names:
			pass


	def _Name(s, id, ctx):
		if id == 'None':
			return NoneLiteral()
		#ctx *should* be ignorable
		return s.getVarNamed(id)

	def _Attribute(s, value, attr, ctx):
		obj = s.translateExpr(value)
		return Attr(s.getNewTemporary(), obj, attr)

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
		obj = s.translateExpr(value)
		if isinstance(slice, ast.Index):
			index = s.translateExpr(slice.value)
			return s.op(Subscript)(obj, index)

		elif isinstance(slice, ast.Slice):
			start, end, step = s.translateSlice(slice)
			return s.op(Slice)(obj, start, end, step)

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
				irtarget = s.getTargetNamed(target.id)
				s.emit(Assign(irtarget, irrhs))
				
			elif isinstance(target, ast.Attribute):
				#we're not assigning to the target, so we don't add it to locals
				irobj = s.translateExpr(target.value)
				s.emit(AssignAttr(irobj, target.attr, irrhs))
				
			elif isinstance(target, ast.Subscript):
				obj = s.translateExpr(target.value)

				if isinstance(target.slice, ast.Index):
					index = s.translateExpr(target.slice.value)
					s.emit(AssignSubscript(obj, index, irrhs))
				
				elif isinstance(target.slice, ast.Slice):
					start, end, step = s.translateSlice(target.slice)
					s.emit(AssignSlice(obj, start, end, step, irrhs))
				
				else:
					raise NotImplementedError
			
			elif type(target) in [ast.List, ast.Tuple]:
				unpackAsgns.append(target.elts)
			
		if len(unpackAsgns) > 0:
			#FIXME: wrong error would be thrown on unpacking
			#wrong # of compoents at runtime, I think.  May want to add OP
		
			iterator = s.getNewTemporary()
			s.emit(Iter(target=iterator, arg=irrhs))
			componentCount = len(unpackAsgns[0])
			if not all([len(upa) == componentCount for upa in unpackAsgns]):
				#TODO: make this runtime?
				s.error('too many/not enough values to unpack')
			
			componentsTargets = zip(*unpackAsgns)
			for cAsgn in componentsTargets:
				component = s.getNewTemporary()
				s.emit(Next(target=component, arg=iterator))
				s.makeAssignment(cAsgn, component)


