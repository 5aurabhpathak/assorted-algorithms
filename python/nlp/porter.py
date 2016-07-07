#!/bin/env python3.5
#Porter's Stemming algorithm (with subtle enhancements)
#Author: Saurabh Pathak
import re, sys

def printUsage():
    print('Usage: porter.py [-v | V] [-f file] [-s string]')

verbose = False
    
class Word:
    def __init__(self, w):
        if type(w) == str:
            self.w = list(w.upper())
        elif type(w) in {list, set, frozenset, tuple}:
            self.w = [c.upper() for c in w]

    def __len__(self):
        return len(self.w)

    def __str__(self):
        st = ""
        for c in self.w:
            st += c
        return st

    @property
    def vcstring(self):
        cvstring = ""
        if self.w[0] not in 'AEIOU': cvstring += 'C'
        else: cvstring += 'V'
        for i in range(1, len(self)):
            if cvstring[-1] == 'C' and self.w[i] in 'AEIOUY': cvstring += 'V'
            elif cvstring[-1] == 'V' and self.w[i] not in 'AEIOU': cvstring += 'C'
        return cvstring
    
    @property
    def m(self):
        m = 0;
        for char in self.vcstring:
            if char == 'V': m += 1
        if self.vcstring[-1] == 'V': m -= 1
        return m

class Porter:
    @classmethod
    def stem(cls, Word):
        if len(Word) >= 4:
            cls.__step1a(Word)
            cls.__step1b(Word)
            cls.__step1c(Word)
            cls.__step2(Word)
            cls.__step3(Word)
            cls.__step4(Word)
            cls.__step5a(Word)
            cls.__step5b(Word)

    def __step1a(Word):
        if Word.w[-4:] == list('SSES') or Word.w[-3:] == list('IES'): del Word.w[-2:]
        elif Word.w[-2:] == list('SS'): pass
        elif Word.w[-1] == 'S': del Word.w[-1]
        if verbose: print('After 1a: {} : {} : {}'.format(Word, Word.vcstring, Word.m))

    def __step1b(wrd):
        flag, test = False, True
        try:
            if wrd.w[-3:] == list('EED'):
                if Word(wrd.w[:-3]).m > 0: wrd.w[-3:] = list('EE')
                test = False
        except: pass
        try:
            if test and wrd.w[-2:] == list('ED'):
                if 'V' in Word(wrd.w[-2:]).vcstring: del wrd.w[-2:]
                flag, test = True, False
        except: pass
        try:
            if test and wrd.w[-3:] == list('ING'):
                if 'V' in Word(wrd.w[:-3]).vcstring: del wrd.w[-3:]
                flag = True
        except: pass
        if flag:
            test = True
            try:
                if wrd.w[-2:] in [list('AT'), list('BL'), list('IZ')]:
                    wrd.w += 'E'
                    test = False
            except: pass
            try:
                if test and wrd.w[-1] == wrd.w[-2] and wrd.w[-1] not in 'LSZ':
                    del wrd.w[-1]
                    test = False
            except: pass
            try:
                if test and wrd.m == 1 and wrd.vcstring[-3:] == 'CVC' and wrd.w[-1] not in 'WXY': wrd.w += 'E'
            except:pass
        if verbose: print('After 1b: {} : {} : {}'.format(wrd, wrd.vcstring, wrd.m))

    def __step1c(wrd):
        try:
            if 'V' in Word(wrd.w[:-1]).vcstring and wrd.w[-1] == 'Y': wrd.w[-1] = 'I'
        except: pass
        if verbose: print('After 1c: {} : {} : {}'.format(wrd, wrd.vcstring, wrd.m))

    def __step2(wrd):
        test = True
        try:
            if wrd.w[-7:] in [list('ATIONAL'), list('IZATION'), list('IVENESS')]:
                if Word(wrd.w[:-7]).m > 0: wrd.w[-5:] = 'E'
                test = False
            elif wrd.w[-7:] in [list('FULNESS'), list('OUSNESS')]:
                if Word(wrd.w[:-7]).m > 0: del wrd.w[-4:]
                test = False
        except: pass
        try:
            if test and wrd.w[-6:] == list('TIONAL'):
                if Word(wrd.w[:-6]).m > 0: del wrd.w[-2:]
                test = False
            elif test and wrd.w[-6:] == list('BILITI'):
                if Word(wrd.w[:-6]).m > 0: wrd.w[-5:] = list('LE')
                test = False
        except: pass
        try:
            if test and wrd.w[-5:] in [list('ENTLI'), list('OUSLI')]:
                if Word(wrd.w[:-5]).m > 0: del wrd.w[-2:]
                test = False
            elif test and wrd.w[-5:] in [list('ALISM'), list('ALITI')]:
                if Word(wrd.w[:-5]).m > 0: del wrd.w[-3:]
                test = False
            elif test and wrd.w[-5:] in [list('ATION'), list('IVITI')]:
                if Word(wrd.w[:-5]).m > 0: wrd.w[-3:] = 'E'
                test = False
        except: pass
        try:
            if test and wrd.w[-4:] in [list('ENCI'), list('ANCI'), list('ABLI')]:
                if Word(wrd.w[:-4]).m > 0: wrd.w[-1] = 'E'
                test = False
            elif test and wrd.w[-4:] in [list('IZER'), list('ATOR')]:
                if Word(wrd.w[:-4]).m > 0: wrd.w[-2:] = 'E'
                test = False
            elif test and wrd.w[-4:] == list('ALLI'):#IMPROVEMENT 1: changed m >0 to >=0
                if Word(wrd.w[:-4]).m >= 0: del wrd.w[-2:]
                test = False
            elif test and wrd.w[-4:] == list('LOGI'):#IMPROVEMENT 2: added (m>=0)LOGI-->null
                if Word(wrd.w[:-4]).m == 0: del wrd.w[-4:]
                test = False
        except: pass
        try:
            if test and wrd.w[-3:] == list('ELI'):
                if Word(wrd.w[:-3]).m > 0: del wrd.w[-2:]
                test = False
        except: pass
        if verbose: print('After 2: {} : {} : {}'.format(wrd, wrd.vcstring, wrd.m))

    def __step3(wrd):
        test = True
        try:
            if wrd.w[-5:] in [list('ICATE'), list('ALIZE'), list('ICITI')]:
                if Word(wrd.w[:-5]).m > 0: del wrd.w[-3:]
                test = False
            elif wrd.w[-5:] in [list('ATIVE'), list('OLOGI')]:#IMPROVEMENT 3: added OLOGI-->null
                if Word(wrd.w[:-5]).m > 0: del wrd.w[-5:]
                test = False
        except: pass
        try:
            if test and wrd.w[-4:] == list('ICAL'):
                if Word(wrd.w[:-4]).m > 0: del wrd.w[-2:]
                test = False
            elif test and wrd.w[-4:] in [list('NESS'), list('LESS')]:
                if Word(wrd.w[:-4]).m > 0: del wrd.w[-4:]
                test = False
        except: pass
        try:
            if test and Word(wrd.w[:-3]).m > 0 and wrd.w[-3:] == list('FUL'): del wrd.w[-3:]
        except: pass
        try:
            if test and wrd.w[-3:] == list('EST'): #IMPROVEMENT 4: added EST --> E
                if Word(wrd.w[:-3]).m > 0: del wrd.w[-2:]
                test = False
        except: pass
        if verbose: print('After 3: {} : {} : {}'.format(wrd, wrd.vcstring, wrd.m))

    def __step4(wrd):
        test = True
        try:
            if wrd.w[-5:] == list('EMENT'):
                if Word(wrd.w[:-5]).m > 1: del wrd.w[-5:]
                test = False                              
        except: pass                                      
        try:#IMPROVEMENT 5: added HOOD-->null
            if test and wrd.w[-4:] in [list('ANCE'), list('ENCE'), list('ABLE'),
                                       list('IBLE'), list('MENT'), list('HOOD')]:
                if Word(wrd.w[:-4]).m > 1: del wrd.w[-4:]
                test = False
        except: pass
        try:
            if test and wrd.w[-3:] in [list('ANT'), list('ENT'), list('ISM'), list('ATE'),
                                       list('ITI'), list('OUS'), list('IVE'), list('IZE'),]:
                if Word(wrd.w[:-3]).m > 1: del wrd.w[-3:]
                test = False
        except: pass
        try:
            if test and wrd.w[-3:] == list('ION'):
                if Word(wrd.w[:-3]).m > 1 and wrd.w[-4] in 'ST': del wrd.w[-3:]
                test = False
        except: pass
        try:
            if test and wrd.w[-2:] == list('AN'):#IMPROVEMNT 6: added AN-->A
                if Word(wrd.w[:-3]).m > 1 : del wrd.w[-1]
                test = False
        except: pass
        try:
            if test and Word(wrd.w[:-2]).m > 1 and wrd.w[-2:] in [list('AL'), list('ER'),
                                                                  list('IC'), list('OU'),
                                                                  ]: del wrd.w[-2:]
        except: pass
        if verbose: print('After 4: {} : {} : {}'.format(wrd, wrd.vcstring, wrd.m))

    def __step5a(wrd):
        test = True
        try:
            if wrd.w[-1] == 'E':
                if Word(wrd.w[:-1]).m > 1: del wrd.w[-1]
                elif Word(wrd.w[:-1]).m == 1 and not (Word(wrd.w[:-1]).vcstring[-3:] == 'CVC' and wrd.w[-2] not in 'WXY'): del wrd.w[-1]
        except: pass
        if verbose: print('After 5a: {} : {} : {}'.format(wrd, wrd.vcstring, wrd.m))

    def __step5b(Word):
        try:
            if Word.m > 1 and Word.w[-1] == Word.w[-2] and Word.w[-1] == 'L': del Word.w[-1]
        except: pass
        try:
            if Word.w[-1] == 'I': Word.w[-1] = 'Y'#IMPROVEMENT 7: final touch. added *I-->*Y
        except: pass
        if verbose: print('After 5b: {} : {} : {}'.format(Word, Word.vcstring, Word.m))


def fromFile(file):
    for line in open(file):
        for word in re.split('\W*\d+\W*|\W+', line):
            if word != '':
                fromString(word)

def fromString(s):
    w = Word(s)
    if verbose: print('{} : {} : {}'.format(w, w.vcstring, w.m))
    else: print(w, end='')
    Porter.stem(w)
    if verbose: print('Stemmed to {}\n'.format(w))
    else: print('-->', w)

if len(sys.argv) == 3:
    if sys.argv[1].lower() == '-f': fromFile(sys.argv[2])
    elif sys.argv[1].lower() == '-s': fromString(sys.argv[2])
    else: printUsage()
elif len(sys.argv) == 4:
    if sys.argv[1].lower() in {'-v', '--verbose'}:
        verbose = True
        if sys.argv[2].lower() == '-f': fromFile(sys.argv[3])
        elif sys.argv[2].lower() =='-s': fromString(sys.argv[3])
    else:
        printUsage()
else: printUsage()
