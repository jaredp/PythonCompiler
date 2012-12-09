from p3 import moduleNamed

BuiltinFn, buildModule = moduleNamed('time')

BuiltinFn('clock', 'P3time_clock')


buildModule()