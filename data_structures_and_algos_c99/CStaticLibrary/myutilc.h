/* 
 * File:   myutilc.h
 * Author: Saurabh
 *
 * Created on 5 July, 2015, 8:55 PM
 */

#ifndef MYUTILC_H
#define	MYUTILC_H

#ifdef	__cplusplus
extern "C" {
#endif
    
#define def_dynamic_array(type, typeid) typedef struct d_##typeid##_array  {   \
unsigned long size; \
unsigned long used; \
type *p;    \
} DArr_##typeid;    \
extern DArr_##typeid initialize_##typeid(unsigned long);    \
extern void put_##typeid(type, DArr_##typeid *);    \
extern void fill_##typeid(type, DArr_##typeid *);   \
extern type get_##typeid(unsigned long, DArr_##typeid *); \
extern void put_##typeid##_at(unsigned long, type, DArr_##typeid *);

    def_dynamic_array(int, int)
    def_dynamic_array(float, float)
    def_dynamic_array(double, double)
    def_dynamic_array(short, short)
    def_dynamic_array(long, long)
    def_dynamic_array(unsigned long, ulong)
    def_dynamic_array(unsigned short, ushort)
    def_dynamic_array(char *, string)
    def_dynamic_array(char, char)
            
#ifdef	__cplusplus
}
#endif

#endif	/* MYUTILC_H */

