/* 
 * File:   test.c
 * Author: Saurabh
 *
 * Created on 8 July, 2015, 8:24 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include "myutils.h"

/*
 * 
 */
int main() {
    uint_fast64_t num;
    printf("Enter number:\n");
    fflush(stdout);
    scanf("%llu", &num);
    bigDArr_uintf64 res = sieve_of_eratosthenes_uintf64(num);
    displaybig_uintf64(&res);
    printf("\nsize grown to:%llu\nused elements: %llu", res.size, res.used);
    return (EXIT_SUCCESS);
}