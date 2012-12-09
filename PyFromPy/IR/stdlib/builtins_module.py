from p3 import moduleNamed

BuiltinFn, buildModule = moduleNamed('__builtin__')

BuiltinFn('len', 'P3__builtin__len', 'seq')


buildModule()
