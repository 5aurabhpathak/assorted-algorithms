#!/bin/env python3.6
#Author: Saurabh Pathak
'''parallel corpus cleaner -- three stage'''
import enchant
from os import makedirs, chdir

def clean():
    '''stage 1 - hindi source sentences containing english letters are dropped (along with corresponding english target sentence)
    stage 2 - heuristic: sentence pairs differing greatly in size are probably misaligned and/or malformed. Prefer over moses's clean-corpus-n script. This function handles size difference more elaborately.
    stage 3 - target side spell checking. Sentence pair is dropped without bothering about correction.'''

    print('Cleaning...', end='', flush=True)
    prohibited_hi = 'abcdefghijklmnopqrstuvwxyz'
    dicts = [enchant.Dict(x) for x in enchant.list_languages() if 'en' in x]
    makedirs('filtered_out', mode=0o755, exist_ok=True)

    with open('parallel/IITB.en-hi.true.en', encoding='utf-8') as en_ip, open('parallel/IITB.en-hi.true.hi', encoding='utf-8') as hi_ip, open('IITB.en-hi.clean.en', 'w', encoding='utf-8') as en_op, open('IITB.en-hi.clean.hi', 'w', encoding='utf-8') as hi_op, open('filtered_out/IITB.en-hi.hi.err', 'w', encoding='utf-8') as hi_err_op, open('filtered_out/IITB.en-hi.en.err', 'w', encoding='utf-8') as en_err_op:

        for hi_line, en_line in zip(hi_ip, en_ip):
            #stage 1
            flag = False
            for c in prohibited_hi:
                if c in hi_line or c.upper() in hi_line:
                    flag = True
                    break
            if flag:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            
            #stage 2
            e, h = en_line.split(), hi_line.split()
            j, k = len([x for x in h if len(x) > 1]), len([x for x in e if len(x) > 1])
            if j == 0 or j > 100 or k == 0 or k > 100 or j > 2 * k or 2 * j < k:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue

            #stage 3
            en_line_tok = {x for x in e if len(x) > 1 and not x.isupper()}
            for d in dicts:
                misspelled = False
                for tok in en_line_tok:
                    #this is why we truecased english data earlier; not only to lowercase later.
                    if not d.check(tok) and tok[0].islower(): #<--checks for proper nouns and abbreviations
                        misspelled = True
                        break
                if not misspelled: break
            if misspelled:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue

            hi_op.write(" ".join(h)) #<--removes redundant spaces.
            en_op.write(" ".join([x.lower() for x in e])) #<--removes redundant spaces, lowercases everything. it is required for training.
    print('complete')

if __name__ == '__main__':
    clean()
