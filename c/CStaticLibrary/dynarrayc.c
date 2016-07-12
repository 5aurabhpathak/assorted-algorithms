/* 
 * File:   dynarrayc.c
 * Author: Saurabh
 *
 * Created on 5 July, 2015, 11:53 PM
 */

#include <stdlib.h>
#include <stdio.h>
#include "mydarrs.h"

#define str(x) #x
#define utils(type, typeid, printformat) DArr_##typeid initialize_##typeid(sub s)   {   \
DArr_##typeid d;   \
d.size = s; \
d.used = 0; \
d.p = NULL;\
while(d.p == NULL)  \
d.p = (type *) malloc(s * sizeof(type)); \
return d;   \
}   \
void put_##typeid(type element, DArr_##typeid * d) {   \
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
void fill_##typeid(type filler, DArr_##typeid * d)    {   \
sub i;    \
type * currentpos;    \
for(i = 0, currentpos = d->p; i < d->size; i++, currentpos++)   \
    *currentpos = filler;   \
d->used = d->size;  \
}   \
type get_##typeid(sub pos, DArr_##typeid * d)   {   \
type * loc = d->p + pos; \
return *loc;    \
}   \
void put_##typeid##_at(sub pos, type element, DArr_##typeid * d)  {   \
type * loc = d->p + pos; \
*loc = element; \
}   \
void display_##typeid(DArr_##typeid * d)    {   \
sub i;    \
printf("%lu\n,", 1234567889ul);    \
for(i = 0; i < d->used ; i++)    \
printf(str(%printformat\t), get_##typeid(i, d)); \
}
/*
 * 
 */
utils(int, int, d)
utils(short, short, hd)
utils(unsigned int, uint, u)
utils(unsigned long, ulong, lu)
utils(unsigned short, ushort, hu)
utils(float, float, f)
utils(double, double, f)
utils(long double, ldouble, Lf)
utils(char *, string, s)
utils(char, char, c)
utils(long, long, ld)
        
#if __STDC_VERSION__ >= 199901L
utils(long long, longlong, lld)
utils(unsigned long long, ulonglong, llu)
#endif