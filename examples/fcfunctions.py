
from __builtin__ import type
def fn(x):
	pass

print fn
fn.a = 9
print fn.a + 1

t = type(fn)
print t
print type(t)
t.a = 4
print t.a + 1

