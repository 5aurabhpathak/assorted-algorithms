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
    
#if (defined __cplusplus && __cplusplus >= 201103L) || __STDC_VERSION__ >= 199901L
    #define sub unsigned long long
    #define subid(x) x##_ulonglong
#else
    #define sub unsigned long
    #define subid(x) x##_ulong
#endif
    
#define def_dynamic_array(type, typeid) typedef struct d_##typeid##_array  {   \
sub size, used; \
type *p;    \
} DArr_##typeid;    \
extern DArr_##typeid initialize_##typeid(sub);    \
extern type get_##typeid(sub, DArr_##typeid *); \
extern void put_##typeid##_at(sub, type, DArr_##typeid *);    \
extern void put_##typeid(type, DArr_##typeid *);    \
extern void fill_##typeid(type, DArr_##typeid *);   \
extern void display_##typeid(DArr_##typeid *);

#if (defined __cplusplus &&  __cplusplus >= 201103L) || __STDC_VERSION__ >= 199901L
    def_dynamic_array(long long, longlong)
    def_dynamic_array(unsigned long long, ulonglong)
#endif
            
    def_dynamic_array(int, int)
    def_dynamic_array(float, float)
    def_dynamic_array(double, double)
    def_dynamic_array(short, short)
    def_dynamic_array(long, long)
    def_dynamic_array(unsigned long, ulong)
    def_dynamic_array(unsigned short, ushort)
    def_dynamic_array(char *, string)
    def_dynamic_array(char, char)
    def_dynamic_array(unsigned int, uint)
    def_dynamic_array(long double, ldouble)

#ifdef	__cplusplus
}
#endif

#endif	/* MYUTILC_H */