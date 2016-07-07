#Plugin routines for Lappin and Leasse algorithm
#Author: Saurabh Pathak
from classes import Entity, ispleonastic
from nltk.tree import ParentedTree

def halve():
    global entitySet
    entitySet = {entity for entity in entitySet if entity.salience != 0}
    for entity in entitySet: entity.salience //= 2

entitySet = set()
def lappinleasse(parsetree, i):
    global entitySet
    for np in parsetree.subtrees(lambda x: x.label() == 'NP'):
        if 'PRP' in np[0].label():
            if np[0,0].lower() == 'it' and ispleonastic(np, parsetree): continue
            maxsalience = -1
            referent = None
            e = Entity(np, parsetree, i)
            for entity in entitySet:
                if entity.sentencenum >= i - 4 and e.agreeswith(entity) and maxsalience < entity.salience:
                    maxsalience = entity.salience
                    referent = entity
            try:
                referent.salience += e.salience
                referent.gender = e.gender
                referent.phrases.add(np[0,0] + str(i))
                orig = np[0,0]
                if np[0].label() == 'PRP$':
                    np[0] = ParentedTree.fromstring('(SUB <'+ referent.name + "'s>)")
                    print('PRP$ substitution', orig, '-->', referent.name)
                else:
                    np[0] = ParentedTree.fromstring('(SUB <' + referent.name + '>)')
                    print('PRP substitution', orig, '-->', referent.name)
            except:
                print('No substitution found for ', orig)
                continue

        elif np[0].label() == 'EX': continue
        else: entitySet.add(Entity(np, parsetree, i))
#    print('Discourse model after sentence', i + 1, ':')
#    for entity in entitySet: print(entity)
    halve()
