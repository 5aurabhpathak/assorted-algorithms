#Routines for Hobb's algorithm
#Author: Saurabh Pathak
from collections import deque
from nltk.tree import ParentedTree
from classes import NounPhrase, ispleonastic

def findX(np):
    x = np.parent()
    p = [np]
    while x.label() not in {'S', 'NP'}:
        p += x,
        x = x.parent()
    p += x,
    return x, p[::-1]

def breadth_first(tree):
    queue = deque([(tree,0)])
    while queue:
        node, depth = queue.popleft()
        if isinstance(node, ParentedTree):
            queue.extend((c, depth + 1) for c in iter(node))
            yield node

def breadth_first_left(tree, p):
    queue = deque([(tree,0)])
    while queue:
        node, depth = queue.popleft()
        if isinstance(node, ParentedTree):
            if node in p:
                flag = True
                try:
                    for c in iter(node):
                        if c is p[p.index(node) + 1]:
                            flag = False
                            queue.append((c, depth + 1))
                        if flag: queue.append((c, depth + 1))
                except IndexError: pass
            else: queue.extend((c, depth + 1) for c in iter(node))
            yield node

def breadth_first_no_np(tree, p):
    queue = deque([(tree,0)])
    while queue:
        node, depth = queue.popleft()
        if isinstance(node, ParentedTree) and node.label() != 'NP':
            if node in p:
                flag = False
                try:
                    for c in iter(node):
                        if c is p[p.index(node) + 1]: flag = True
                except IndexError: pass
            else: queue.extend((c, depth + 1) for c in iter(node))
            yield node

def bfs(x, p, np, direction='left'):
    func = breadth_first_no_np if direction == 'right' else breadth_first_left
    for node in func(x, p):
        if node.label() == 'NP' and consider(node, np): return node
    return None

def consider(node, np):
    if NounPhrase(np).agreeswith(NounPhrase(node)): return True
#    print('rejected', NounPhrase(node).name)
    return False

def bfsresolve(np, i):
    if i < 0: return None
    for node in breadth_first(ptlist[i]):
        if isinstance(node, ParentedTree) and node.label() == 'NP' and consider(node, np): return node
    return bfsresolve(np, i-1)

def hobbsresolve(np, i):
    x, p = findX(np)
    node = bfs(x, p, np)
    if node: return node
    if x.parent().label() == 'ROOT': return bfsresolve(np, i-1)
    x, p= findX(x)
    if x.label() == 'NP' and x[0].label() not in {'NNS', 'NNP', 'NNPS', 'NN', 'CD'} and consider(x, np): return x
    node = bfs(x, p, np)
    if node: return node
    if x.label() == 'S': return bfs(x, p, np, 'riht')
    return hobbsresolve(x, i)

ptlist = None
def hobbs(parsetree, i, l):
    global ptlist
    ptlist = l
    for np in parsetree.subtrees(lambda x: x.label() == 'NP'):
        if 'PRP' in np[0].label():
            if np[0,0].lower() == 'it' and ispleonastic(np, parsetree): continue
            referent = hobbsresolve(np, i)
            if not referent: continue
            referent = NounPhrase(referent)
            orig = np[0,0]
            if np[0].label() == 'PRP$':
                np[0] = ParentedTree.fromstring('(PRP$ <'+ referent.name + "'s>)")
                print('PRP$ substitution', orig, '-->', referent.name)
            else:
                np[0] = ParentedTree.fromstring('(PRP <' + referent.name + '>)')
                print('PRP substitution', orig, '-->', referent.name)

