from copy import deepcopy

class Player:
    
    d = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    
    def __init__(self, p):
        if isinstance(p, str):
            self.name = p
            self.pieces = {}
        else:
            self.name = p.name
            self.pieces = deepcopy(p.pieces)
        
    def addPieces(self, n):
        idt = {'Q': 0, 'N': 0, 'R': 0, 'B': 0}
        for i in range(n):
            t = input().strip().split()
            self.pieces.update({t[0]+str(idt[t[0]]): (Player.d[t[1]], int(t[2]))})
            idt[t[0]] += 1
        
    def allMoves(self, P):
        self.pm = {}
        t, s = self.pieces.values(), P.pieces.values()
        for p in self.pieces.items():
            p = p[0], p[1][0], p[1][1]
            if 'N' in p[0]:
                if p[1]+2 <= 4:
                    if p[2]-1 > 0 and (p[1]+2, p[2]-1) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+2, p[2]-1),)})
                    if p[2]+1 <= 4 and (p[1]+2, p[2]+1) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+2, p[2]+1),)})
                if p[1]-2 > 0:
                    if p[2]-1 > 0 and (p[1]-2, p[2]-1) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-2, p[2]-1),)})
                    if p[2]+1 <= 4 and (p[1]-2, p[2]+1) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-2, p[2]+1),)})
                if p[2]+2 <= 4:
                    if p[1]+1 <= 4 and (p[1]+1, p[2]+2) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+1, p[2]+2),)})
                    if p[1]-1 > 0 and (p[1]-1, p[2]+2) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-1, p[2]+2),)})
                if p[2]-2 > 0:
                    if p[1]+1 <= 4 and (p[1]+1, p[2]-2) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+1, p[2]-2),)})
                    if p[1]-1 > 0 and (p[1]-1, p[2]-2) not in t: self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-1, p[2]-2),)})
            else:
                i = 1
                leap_horiz, leap_up_diag, leap_down_diag = False, False, False
                while p[1] + i <= 4:
                    if 'B' not in p[0] and not leap_horiz:
                        if (p[1]+i, p[2]) not in t:
                            self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+i, p[2]),)})
                            if (p[1]+i, p[2]) in s: leap_horiz = True
                        else: leap_horiz = True
                    if 'R' not in p[0]:
                        if p[2] + i <= 4 and not leap_up_diag:
                            if (p[1]+i, p[2]+i) not in t:
                                self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+i, p[2]+i),)})
                                if (p[1]+i, p[2]+i) in s: leap_up_diag = True
                            else: leap_up_diag = True
                        if p[2] - i > 0 and not leap_down_diag:
                            if (p[1]+i, p[2]-i) not in t:
                                self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]+i, p[2]-i),)})
                                if (p[1]+i, p[2]-i) in s: leap_down_diag = True
                            else: leap_down_diag = True
                    i += 1
                i = 1
                leap_horiz, leap_up_diag, leap_down_diag = False, False, False
                while p[1] - i > 0:
                    if 'B' not in p[0] and not leap_horiz:
                        if (p[1]-i, p[2]) not in t:
                            self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-i, p[2]),)})
                            if (p[1]-i, p[2]) in s: leap_horiz = True
                        else: leap_horiz = True
                    if 'R' not in p[0]:
                        if p[2] + i <= 4 and not leap_up_diag:
                            if (p[1]-i, p[2]+i) not in t:
                                self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-i, p[2]+i),)})
                                if (p[1]-i, p[2]+i) in s: leap_up_diag = True
                            else: leap_up_diag = True
                        if p[2] - i > 0 and not leap_down_diag:
                            if (p[1]-i, p[2]-i) not in t:
                                self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1]-i, p[2]-i),)})
                                if (p[1]-i, p[2]-i) in s: leap_down_diag = True
                            else: leap_down_diag = True
                    i += 1
                if 'B' not in p[0]:
                    i = 1
                    leap = False
                    while p[2] + i <= 4 and not leap:
                        if (p[1], p[2]+i) not in t:
                            self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1], p[2]+i),)})
                            if (p[1], p[2]+i) in s: leap = True
                        else: leap = True
                        i += 1
                    i = 1
                    leap = False
                    while p[2] - i > 0 and not leap:
                        if (p[1], p[2]-i) not in t:
                            self.pm.update({p[0]: self.pm.get(p[0], ()) + ((p[1], p[2]-i),)})
                            if (p[1], p[2]-i) in s: leap = True
                        else: leap = True
                        i += 1

def play(player, otherPlayer, m):
    if not m: return 'B'
    #print(player.pieces, otherPlayer.pieces)
    player.allMoves(otherPlayer)
    for values in player.pm.values():
        for value in values:
            if value == otherPlayer.pieces['Q0']: return player.name
    for piece in player.pm.items():
        for move in piece[1]:
            P, O = Player(player), Player(otherPlayer)
            P.pieces.update({piece[0]: move})
            #print(P.pieces, O.pieces)
            for pc, cord in O.pieces.items():
                if cord == move:
                    O.pieces.pop(pc)
                    break
            if play(O, P, m-1) == P.name: return P.name
    return otherPlayer.name

if __name__ == '__main__':
    g = int(input().strip())
    for i in range(g):
        w, b, m = map(int, input().strip().split())
        W, B = Player('W'), Player('B')
        W.addPieces(w)
        B.addPieces(b)
        #print(W.pieces, W.pm)
        print('YES' if play(W, B, m) == 'W' else 'NO')
