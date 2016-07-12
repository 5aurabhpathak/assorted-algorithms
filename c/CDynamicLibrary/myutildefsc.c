/* 
 * File:   myutildefsc.c
 * Author: Saurabh
 *
 * Created on 6 July, 2015, 1:35 AM
 */

#include "myutils.h"

/*
 * 
 */

#define def_funcs(sizeid, typeid, sub)  \
sizeid##DArr_##typeid brute_force_primes_##typeid(sub max) {    \
    sub i, j;   \
    sizeid##DArr_##typeid res = initialize##sizeid##_##typeid(1); \
    sizeid##put_##typeid(1, &res);  \
    for (i = 1; i <= max ; i++) {   \
        for (j = 2; j < i ; j++)    \
            if(i % j == 0)  break;  \
        if(j == i) sizeid##put_##typeid(i, &res); \
    }   \
    return res; \
}   \
/*ushort array here is always big indexed to avoid narrowing when
 *max is big integer
 */  \
    sizeid##DArr_##typeid sieve_of_eratosthenes_##typeid(sub max)   {    \
    bigDArr_char numb = initializebig_char(max);  \
    sizeid##DArr_##typeid res = initialize##sizeid##_##typeid(1); \
    sub current_num, mul, prod; \
    bigfill_char(1, &numb);  \
    sizeid##put_##typeid(1, &res);    \
    for(current_num = 2; current_num <= max ; current_num++)    \
        if(bigget_char(current_num - 1, &numb))   {  \
            sizeid##put_##typeid(current_num, &res);    \
            for(prod = current_num * current_num, mul = current_num;    \
                    prod <= max; prod = current_num * ++mul)    \
                bigput_char_at(prod - 1, 0, &numb);  \
        }   \
    return res; \
}

def_funcs(small, uintf16, uint_fast16_t)
def_funcs(big, uintf64, uint_fast64_t)