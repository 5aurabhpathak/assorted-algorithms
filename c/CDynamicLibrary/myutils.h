/* 
 * File:   myutils.h
 * Author: Saurabh
 *
 * Created on 6 July, 2015, 5:06 PM
 */

#ifndef MYUTILS_H
#define	MYUTILS_H

#ifdef	__cplusplus
extern "C" {
#endif

#include "mydarrs.h"

#define dec_func(sizeid, typeid, type)  \
extern sizeid##DArr_##typeid brute_force_primes_##typeid(type);  \
extern sizeid##DArr_##typeid sieve_of_eratosthenes_##typeid(type);

    /*do not confuse it with bindings in mydarrs.h. These bindings
     *bind the return type array (with always small indices) to the
     *type of entered argument*/
    dec_func(big, uintf64, uint_fast64_t)
    dec_func(small, uintf16, uint_fast16_t)

#ifdef	__cplusplus
}
#endif

#endif	/* MYUTILS_H */