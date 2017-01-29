#!/bin/env python3.6
#Author: Saurabh Pathak
'''
parallel corpus cleaner -- three stage
separate directories are created for intermediate stage files and filtered sentences are also recorded stagewise for study.
should be run by 'clean_corpora.sh'. The shell script also cleans up unused files and directories but leaves filtered stage directories to look at.
'''
import enchant
from os import makedirs, chdir

def stage1():
    '''stage 1 - hindi source sentences containing english letters are dropped (along with corresponding english target sentence)'''

    print('Executing Stage 1...', end='', flush=True)
    prohibited_hi, i = 'abcdefghijklmnopqrstuvwxyz', 0
    makedirs('cleaned_parallel/stage1', mode=0o755, exist_ok=True)
    makedirs('filtered_out/stage1cleaning', mode=0o755, exist_ok=True)

    with open('parallel/IITB.en-hi.true.en', encoding='utf-8') as en_ip, open('parallel/IITB.en-hi.true.hi', encoding='utf-8') as hi_ip, open('cleaned_parallel/stage1/IITB.en-hi.en', 'w', encoding='utf-8') as en_op, open('cleaned_parallel/stage1/IITB.en-hi.hi', 'w', encoding='utf-8') as hi_op, open('filtered_out/stage1cleaning/IITB.en-hi.hi.err', 'w', encoding='utf-8') as hi_err_op, open('filtered_out/stage1cleaning/IITB.en-hi.en.err', 'w', encoding='utf-8') as en_err_op:

        for hi_line, en_line in zip(hi_ip, en_ip):
            flag = False
            for c in prohibited_hi:
                if c in hi_line or c.upper() in hi_line:
                    flag = True
                    break
            if flag:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            hi_op.write(hi_line)
            en_op.write(en_line)
    print('complete')

def stage2():
    '''stage 2 - heuristic: sentence pairs differing greatly in size are probably misaligned and/or malformed. Prefer over moses's clean-corpus-n script. This function handles size difference more elaborately.'''

    print('Executing Stage 2...', end='', flush=True)
    makedirs('cleaned_parallel/stage2', mode=0o755, exist_ok=True)
    makedirs('filtered_out/stage2cleaning', mode=0o755, exist_ok=True)

    with open('cleaned_parallel/stage1/IITB.en-hi.en', encoding='utf-8') as en_ip, open('cleaned_parallel/stage1/IITB.en-hi.hi', encoding='utf-8') as hi_ip, open('cleaned_parallel/stage2/IITB.en-hi.en', 'w', encoding='utf-8') as en_op, open('cleaned_parallel/stage2/IITB.en-hi.hi', 'w', encoding='utf-8') as hi_op, open('filtered_out/stage2cleaning/IITB.en-hi.hi.err', 'w', encoding='utf-8') as hi_err_op, open('filtered_out/stage2cleaning/IITB.en-hi.en.err', 'w', encoding='utf-8') as en_err_op:

        for hi_line, en_line in zip(hi_ip, en_ip):
            j, k = len([x for x in hi_line.split() if len(x) > 1]), len([x for x in en_line.split() if len(x) > 1])
            if j == 0 or j > 100 or k == 0 or k > 100 or j > 2 * k or 2 * j < k:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            hi_op.write(hi_line)
            en_op.write(en_line)
    print('complete')

def stage3():
    '''stage 3 - target side spell checking. Sentence pair is dropped without bothering about correction.'''

    print('Executing Stage 3...', end='', flush=True)
    dicts = [enchant.Dict(x) for x in enchant.list_languages() if 'en' in x]
    makedirs('cleaned_parallel/stage3', mode=0o755, exist_ok=True)
    makedirs('filtered_out/stage3cleaning', mode=0o755, exist_ok=True)

    with open('cleaned_parallel/stage2/IITB.en-hi.en', encoding='utf-8') as en_ip, open('cleaned_parallel/stage2/IITB.en-hi.hi', encoding='utf-8') as hi_ip, open('cleaned_parallel/stage3/IITB.en-hi.en', 'w', encoding='utf-8') as en_op, open('cleaned_parallel/stage3/IITB.en-hi.hi', 'w', encoding='utf-8') as hi_op, open('filtered_out/stage3cleaning/IITB.en-hi.hi.err', 'w', encoding='utf-8') as hi_err_op, open('filtered_out/stage3cleaning/IITB.en-hi.en.err', 'w', encoding='utf-8') as en_err_op:

        for hi_line, en_line in zip(hi_ip, en_ip):
            en_line_tok = {x for x in en_line.split() if len(x) > 1 and not x.isupper()}
            for d in dicts:
                misspelled = False
                for tok in en_line_tok:
                    if not d.check(tok) and tok[0].islower():
                        misspelled = True
                        break
                if not misspelled: break
            if misspelled:
                hi_err_op.write(hi_line)
                en_err_op.write(en_line)
                continue
            hi_op.write(hi_line)
            en_op.write(en_line)
    print('complete')

if __name__ == '__main__':
    chdir('/home/phoenix/src/python/nlp/mtech-thesis/data/corpus/bilingual/')
    stage1()
    stage2()
    stage3()
