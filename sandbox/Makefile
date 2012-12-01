SOURCES = fibpy.cpp

apy++ : $(SOURCES)
	g++	-Wall \
	-I /System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7/ \
	$(SOURCES) -lpython2.7 -o apy++


upy++ : $(SOURCES)
	g++ -I /usr/include/python2.7 -o upy++ $(SOURCES)
	
.PHONY : clean
clean :
	rm -f apy++ upy++
