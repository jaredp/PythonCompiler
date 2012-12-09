APYLIB = /System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/ 
UPYLIB = /usr/include/python2.7
PYLIB = ${UPYLIB}

P3Lib.o : *.h *.cpp
	g++ -c -I ${PYLIB} *.cpp -o P3Lib.o


.PHONY : clean
clean : 
	rm -f P3Lib.o


