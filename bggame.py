# the boardposition
# [whites (npos, n), blacks (npos, n), [n_bar_white, n_bar_black]]
# bar: npos=-1
import functools

class IllegalMoveException(Exception):
    pass

class BgGame:
    def __init__(self):
        self.startpos()

    @staticmethod
    def turnposition(pos):
        """returns a mirrored boardposition
        pos: the boardposition to mirror"""
        return [[(23-x, y) for (x,y) in pos[1]],
                [(23-x, y) for (x,y) in pos[0]],
                [pos[2][1], pos[2][0]]]

    @staticmethod
    def do_one_move(pos, npos, n):
        """move a white piece. if you want to move a black piece use .turnposition() first
        pos: boardposition
        npos: pos of the piece
        n: number of points to move forward
        returns: new boardpos or False if illegal"""
        
        white = dict(pos[0])
        black = dict(pos[1])
        for i in range(24):
            white.setdefault(i, 0)
            black.setdefault(i, 0)
        bar = pos[2][:]

        newpos=npos+n

        if (bar[0]!=0):  # pieces on bar
            if (npos != -1):   # move from bar
                return False
            else:
                if (black[newpos] > 1):    # blocked point
                    return False
                elif (black[newpos] == 1): # beat the piece
                    bar[1] +=1
                    bar[0] -=1
                    white[newpos]=1
                    black[newpos]=0
                else:   # nothing to beat
                    bar[0]-=1
                    white[newpos]+=1
        else:  # normal move
            if (npos == -1):    # nothing on bar
                return False
            if (npos > 23):     # this is no point
                return False
            if (white[npos] == 0):     # no piece to move
                return False

            if (newpos >= 24):   # move out
                if (bar[0] +
                    reduce(lambda x,y:x+y, (white[x] for x in xrange(18))) != 0):  # still pieces around?
                    return False
                else:  # can move out
                    if (newpos == 24):
                        white[npos]-=1
                    else:  # throw too high/wasting move
                        if (reduce(lambda x,y:x+y, (white[x] for x in xrange(npos))) == 0):
                            white[npos]-=1
                        else:
                            return False
            else:
                if (black[newpos] > 1):    # blocked point
                    return False
                elif (black[newpos] == 1): # beat the piece
                    white[npos]-=1
                    white[newpos]+=1
                    black[newpos]=0
                    bar[1]+=1
                else:   # nothing to beat
                    white[npos]-=1
                    white[newpos]+=1

        return [white.items(), black.items(), bar]
                
    @staticmethod
    def possible_move(pos, n):
        """return if there are possible moves for white for a die n (for black, use turnpos)"""
        if (pos[2][0]>0): # piece on bar
            m=BgGame.do_one_move(pos, -1, n)
            if (m!=False):
                return (-1, n)
            else:
                return False
        else:
            for (npos, p) in pos[0]:
                if (p>0):
                    if (BgGame.do_one_move(pos, npos, n)!=False):
                        return [(npos, n)]
                    
        return False

    @staticmethod
    def possible_moves(pos, throw):
        return reduce(lambda a,b:a or b, (BgGame.possible_move(pos, n) for n in throw), False)
        
    def startpos(self):
        """set blackpos and whitepos to startposition"""
       # self.position = [[(18,2), (19,2), (20,2), (21,2), (22,2), (23,2)]]  # testpos

        self.position = [[(0, 2), (11, 5), (16, 3), (18, 5)]]
        self.position.append([(23-x, y) for (x,y) in self.position[0]])
        self.position.append([0,0]) # bar

    def do_move(self, turn, throw, move):
        """turn: 0/1, whose turn is it?
        throw: dicetuple
        move: list as [(npos, npoints), ...]"""
        if (turn==1):  # black
            pos = self.turnposition(self.position)

        if (throw[0]==throw[1]):
            throw=[throw[0]]*4
        else:
            throw=throw[:]

        for (npos, n) in move:
            if (len(throw) == 0):
                raise IllegalMoveException("too many moves")
            
            pos = self.do_one_move(pos, npos, n)
            
            if (pos==False):
                raise IllegalMoveException("illegal move")
            throw.remove(n)  # die used

        if (len(throw)>0 and self.possible_moves(pos, throw)):
            raise IllegalMoveException("not enough moves")

        if (turn==1):  # black
            pos = self.turnposition(pos)

        self.position = pos