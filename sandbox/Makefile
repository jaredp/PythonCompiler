APYLIB = /System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/ 
UPYLIB = /usr/include/python2.7
PYLIB = ${APYLIB}

P3LIB = ../pylib
P3Sources = ../pylib/pylib.cpp
P3OBJ = ../pylib/P3Lib.o

little : little.cpp ${P3OBJ}
	g++ -I ${PYLIB} -I ${P3LIB} little.cpp ${P3OBJ} -lpython2.7 -o little
	
little.cpp : little.py
	py++ little.py > little.cpp

${P3OBJ} : ${P3Sources}
	g++ -I ${PYLIB} -I ${P3LIB} -c ${P3Sources} -lpython2.7 -o ${P3OBJ}

.PHONY : IR
IR : 
	py++ little.py -i

.PHONY : clean
clean :
	rm -f little.cpp little
