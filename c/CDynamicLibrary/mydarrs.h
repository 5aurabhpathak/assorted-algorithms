/* 
 * File:   mydarrs.h
 * Author: Saurabh
 *
 * Created on 5 July, 2015, 8:55 PM
 */

#ifndef MYDARRS_H
#define	MYDARRS_H

#ifdef	__cplusplus
extern "C" {
#endif

#include <stdint.h>

#define def_dynamic_array(type, typeid, sizeid, sizetype) \
typedef struct d_##typeid##_##sizeid##array  {   \
sizetype size, used; \
type *p;    \
} sizeid##DArr_##typeid;    \
extern sizeid##DArr_##typeid initialize##sizeid##_##typeid(sizetype);    \
extern type sizeid##get_##typeid(sizetype, sizeid##DArr_##typeid *); \
extern void sizeid##put_##typeid##_at(sizetype, type, sizeid##DArr_##typeid *);    \
extern void sizeid##put_##typeid(type, sizeid##DArr_##typeid *);    \
extern void sizeid##fill_##typeid(type, sizeid##DArr_##typeid *);   \
extern void display##sizeid##_##typeid(sizeid##DArr_##typeid *);

#define declare(sizeid, sizetype) \
    def_dynamic_array(uint_fast16_t, uintf16, sizeid, sizetype) \
    def_dynamic_array(uint_fast8_t, uintf8, sizeid, sizetype)   \
    def_dynamic_array(uint_fast64_t, uintf64, sizeid, sizetype)  \
    def_dynamic_array(int, int, sizeid, sizetype)   \
    def_dynamic_array(float, float, sizeid, sizetype)   \
    def_dynamic_array(double, double, sizeid, sizetype) \
    def_dynamic_array(short, short, sizeid, sizetype)   \
    def_dynamic_array(long, long, sizeid, sizetype) \
    def_dynamic_array(unsigned long, ulong, sizeid, sizetype)   \
    def_dynamic_array(unsigned short, ushort, sizeid, sizetype) \
    def_dynamic_array(char *, string, sizeid, sizetype) \
    def_dynamic_array(char, char, sizeid, sizetype) \
    def_dynamic_array(unsigned int, uint, sizeid, sizetype) \
    def_dynamic_array(long double, ldouble, sizeid, sizetype)

    /*Determines maximum acheivable size of arrays
     *as the types mentioned are used for storing index values
     *do not change these bindings. if you do, do it at all places in the
     *source and recompile the library before using this header*/
    declare(small, uint_fast32_t)
    declare(big, uint_fast64_t)

#ifdef	__cplusplus
}
#endif

#endif	/* MYUTILC_H */