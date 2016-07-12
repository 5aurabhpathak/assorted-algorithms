/* 
 * File:   dynarrayc.c
 * Author: Saurabh
 *
 * Created on 5 July, 2015, 11:53 PM
 */

#include <stdlib.h>
#include <stdio.h>
#include "mydarrs.h"
#include <stdint.h>

#define str(x) #x
#define utils(type, typeid, printformat, sizeid, sizetype) \
sizeid##DArr_##typeid initialize##sizeid##_##typeid(sizetype s)   {   \
sizeid##DArr_##typeid d;   \
d.size = s; \
d.used = 0; \
d.p = NULL;\
while(d.p == NULL)  \
d.p = (type *) malloc(s * sizeof(type)); \
return d;   \
}   \
void sizeid##put_##typeid(type element, sizeid##DArr_##typeid * d) {   \
type * loc;   \
if(d->used == d->size) {\
    d->size *= 2;   \
    do loc = (type *) realloc(d->p, d->size * sizeof(type));  \
    while(loc == NULL); \
    d->p = loc; \
    }\
loc = d->p + d->used++; \
*loc = element; \
}   \
void sizeid##fill_##typeid(type filler, sizeid##DArr_##typeid * d)    {   \
sizetype i;    \
type * currentpos;    \
for(i = 0, currentpos = d->p; i < d->size; i++, currentpos++)   \
    *currentpos = filler;   \
d->used = d->size;  \
}   \
type sizeid##get_##typeid(sizetype pos, sizeid##DArr_##typeid * d)   {   \
type * loc = d->p + pos; \
return *loc;    \
}   \
void sizeid##put_##typeid##_at(sizetype pos, type element, sizeid##DArr_##typeid * d)  {   \
type * loc = d->p + pos; \
*loc = element; \
}   \
void display##sizeid##_##typeid(sizeid##DArr_##typeid * d)    {   \
sizetype i;    \
for(i = 0; i < d->used ; i++)   \
printf(str(%printformat\t), sizeid##get_##typeid(i, d)); \
}
/*
 * 
 */

#define def_utils(sizeid, sizetype) \
    utils(int, int, d, sizeid, sizetype)    \
    utils(short, short, hd, sizeid, sizetype)   \
    utils(unsigned int, uint, u, sizeid, sizetype)  \
    utils(unsigned long, ulong, lu, sizeid, sizetype)   \
    utils(unsigned short, ushort, hu, sizeid, sizetype) \
    utils(float, float, f, sizeid, sizetype)    \
    utils(double, double, f, sizeid, sizetype)  \
    utils(long double, ldouble, Lf, sizeid, sizetype)   \
    utils(char *, string, s, sizeid, sizetype)  \
    utils(char, char, c, sizeid, sizetype)  \
    utils(long, long, ld, sizeid, sizetype) \
    utils(uint_fast16_t, uintf16, u, sizeid, sizetype)  \
    utils(uint_fast8_t, uintf8, u, sizeid, sizetype)    \
    utils(uint_fast64_t, uintf64, llu, sizeid, sizetype)

def_utils(small, uint_fast32_t)
def_utils(big, uint_fast64_t)