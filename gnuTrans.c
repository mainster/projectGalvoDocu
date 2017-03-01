#include <stdio.h>
#include <stdint.h>
#include "gnu.h"


int main (void) {
	for (uint8_t line = 0; line < sizeof(gnu)/sizeof(gnu[0]); line++) {
		printf("Seg %i:\t%5.3g\t%5.3g\t%5.3g\t%5.3g\n", 
		       line, gnu[line][0][0], gnu[line][0][1], gnu[line][1][0], gnu[line][1][1]);
	}

	return 0;
}