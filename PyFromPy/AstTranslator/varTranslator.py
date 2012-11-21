
from IR import ir

class VarTranslator:
	def _Global(s, names):
		if s.isInGlobalBlock():
			s.error("global declaration in global scope")
		
		for name in names:
			pass
	
	def _Del(s, targets):
		for target in targets:
			if isinstance(target, ast.Name):
				var = s.getTargetNamed(target.id)
				s.emit(ir.DeleteVar(var))
				
			elif isinstance(target, ast.Attribute):
				irobj = s.translateExpr(target.value)
				op = ir.DeleteAttr(target=irobj, attr=target.attr)
				
			elif isinstance(target, ast.Subscript):
				pass	# FIXME!
				
			elif type(target) in [ast.List, astTuble]:
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
				op = ir.Assign(irtarget, irrhs)
				
			elif isinstance(target, ast.Attribute):
				#we're not assigning to the target, so we don't add it to locals
				irobj = s.translateExpr(target.value)
				op = ir.AttrSetter(target=irobj, attr=target.attr, rhs=irrhs)
				
			elif isinstance(target, ast.Subscript):
				pass # FIXME!
			
			elif type(target) in [ast.List, ast.Tuple]:
				unpackAsgns.append(target.elts)
				continue
			
			s.emit(op)
			
		if len(unpackAsgns) > 0:
			#FIXME: wrong error would be thrown on unpacking
			#wrong # of compoents at runtime, I think.  May want to add OP
		
			iterator = s.getNewTemporary()
			s.emit(ir.Iter(target=iterator, arg=irrhs))
			componentCount = len(unpackAsgns[0])
			if not all([len(upa) == componentCount for upa in unpackAsgns]):
				#TODO: make this runtime?
				s.error('too many/not enough values to unpack')
			
			componentsTargets = zip(*unpackAsgns)
			for cAsgn in componentsTargets:
				component = s.getNewTemporary()
				s.emit(ir.Next(target=component, arg=iterator))
				s.makeAssignment(cAsgn, component)


