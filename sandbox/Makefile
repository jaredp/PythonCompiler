APYLIB = /System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/ 
UPYLIB = /usr/include/python2.7
PYLIB = ${APYLIB}

P3LIB = ../pylib

little : little.cpp
	g++ -I ${PYLIB} -I ${P3LIB} little.cpp -o little
	
little.cpp : little.py
	py++ little.py > little.cpp

.PHONY : clean
clean :
	rm -f little.cpp little
