from p3 import moduleNamed

BuiltinFn, buildModule = moduleNamed('__builtin__')

BuiltinFn('len', 'P3__builtin__len', 'seq')
BuiltinFn('raw_input', 'P3__builtin__raw_input', 'prompt')
BuiltinFn('int', 'P3__builtin__int', 'value')

buildModule()
