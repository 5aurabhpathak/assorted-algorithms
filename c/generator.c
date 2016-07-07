/*
 *Generates extremly large unsorted file for processing by external
 *sorting algorithm
 *
 *This code generates 64 bit random numbers by using rand() function
 *and bit wise leftshift. rand() generates 32bit(or fewer) integers on most
 *systems so we need multiple calls
 *
 *~Phoenix~
 */

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

unsigned long long ullrand();

/*Required size in bytes*/
const unsigned long long FILESIZEINBYTES = 1024 * 1024 * 1024 * 10ull;
int leftshift;
int iterations;

/*
 *RAND_MAX is defined to be at least 16bits but
 *maybe longer and is usually is. We need to find the right amount of
 *shift. We also need to find the number of calls to rand() necessary to
 *randomly fill all 64bits of a number.
 */
int main()
{
	srand(time(NULL));
	leftshift = sizeof(RAND_MAX) * 8;
	iterations = ceil(64 / leftshift);

	long long unsigned written;
	written = 0;
	while (written < FILESIZEINBYTES)
		written += printf("%llu\n", ullrand());
}

unsigned long long ullrand()
{
	long long unsigned r;
	for (int i = 0; i < iterations; i++)
		r = (r << leftshift) | rand();

	return r & 0xFFFFFFFFFFFFFFFFull;
}

/*PS: This is a general code designed to run on any machine
 *if you know that sizeof(RAND_MAX) is 4 byte on your machine then
 *above code is simplified. ;)
 */
