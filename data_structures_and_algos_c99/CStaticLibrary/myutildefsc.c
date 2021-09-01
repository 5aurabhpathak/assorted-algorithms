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

subid(DArr) brute_force_primes (sub max) {
    sub i, j;
    subid(DArr) res = subid(initialize)(1);
    subid(put)(1, &res);
    for (i = 1; i <= max ; i++) {
        for (j = 2; j < i ; j++)
            if(i % j == 0)  break;
        if(j == i) subid(put)(i, &res);
    }
    return res;
}

subid(DArr) sieve_of_eratosthenes(sub max)   {
    DArr_ushort numb = initialize_ushort(max);
    subid(DArr) res = subid(initialize)(1);
    sub current_num, mul, prod;
    fill_ushort(1, &numb);
    subid(put)(1, &res);
    for(current_num = 2; current_num <= max ; current_num++)
        if(get_ushort(current_num - 1, &numb))   {
            subid(put)(current_num, &res);
            for(prod = current_num * current_num, mul = current_num;
                    prod <= max; prod = current_num * ++mul)
                put_ushort_at(prod - 1, 0, &numb);
        }
    return res;
}