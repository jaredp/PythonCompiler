
#include <stdio.h>
#include <time.h>

/* PRINT */

void print(void *loc, const char *str) {
	printf("%s ", str);
}

void print(void *loc, double fl) {
	printf("%lf ", fl);
}

void print(void *loc, long i) {
	printf("%ld ", i);
}

void print(void *loc, int i) {
	printf("%d ", i);
}

void print(void *loc, float fl) {
	printf("%f ", fl);
}

void printnl(void) {
	printf("\n");
}

/* TIME PROFILING */

float fclock() {
	return ((float)clock()) / (float)CLOCKS_PER_SEC;
}
