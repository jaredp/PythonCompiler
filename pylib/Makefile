APYLIB = /System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/ 
UPYLIB = /usr/include/python2.7
PYLIB = ${UPYLIB}

%.o : %.cpp *.h
	g++ -g -c -I ${PYLIB} $< -o $@

SRCS=$(wildcard *.cpp)
OBJS=$(SRCS:.cpp=.o)

libP3.a : $(OBJS)
	ar cr libP3.a $?


.PHONY : clean
clean : 
	rm -f *.o *.a


