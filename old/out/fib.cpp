
/*
 * generated from source python by the py++ compiler
 * by Jared Pochtar and Abhas Bodas
 * available at github.com/jaredp/PythonCompiler
 */

#include "../pylib/pylibs.h"



const char *fib__doc = "fib computes the nth number of the fibonacci sequence";
int fib(int n) {
	if ((n == 1)) {
		return 1;
	}
	else if ((n == 2)) {
		return 1;
	}
	else {
		" base cases covered ";
		return (fib((n - 1)) + fib((n - 2)));
	}
}

int m() {
	int i$0;
	int start$1;
	int sum$2;
	int end$3;
	start$1 = fclock();
	sum$2 = 0;
	i$0 = 1;
	while (i$0 < 35) {
		sum$2 += fib(i$0);
		i$0 += 1;
	}
	end$3 = fclock();
	print(None, sum$2);
	print(None, ", found in");
	print(None, (end$3 - start$1));
	print(None, "seconds");
	printnl();
}

int load() {
	m();
}

#include <stdio.h>

int main(int argc, char **argv) {
	float start = fclock();
	load();
	float end = fclock();
	printf("\nin %f seconds\n", end - start);
}



