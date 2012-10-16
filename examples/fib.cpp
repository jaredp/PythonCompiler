
#import <iostream>
#import <time.h>

int fib(int n) {
    if (n == 1) {
        return 1;
    } else if (n == 2) {
        return 1;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}

int main(int argc, char **argv) {
    int start = clock();
    
    long sum = 0;
    for (int i = 1; i < 35; i++) {
        sum += fib(i);
    }
    
    int end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    std::cout << sum << ", found in " << seconds << " seconds\n";
}
