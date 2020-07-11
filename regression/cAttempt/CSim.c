#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

 
#define MAX3(a, b, c) (((c) > (a) && (c) > (b)) ? (c) : ((b) > (a) ? (b) : (a)))

int testFunction(int a[], int count ) {
	int sum = 0;
	for(int i = 0; i < 3; i++) {
		sum += a[i];
	}
	return sum;
}


int main()
{
	return 0;
}