import pygame
import sys
from pygame.locals import *
import random
import copy
import time
import atexit

import menu
import mopgi
import bggame
import ingamemenu
import roll
import network
import sound
import configuration

##################################################
# how does the board work?
# the screen is 4:3
# upper left: 6 points with width=screenwidth/15 (to 6/15)
# then the bar (1/15) -> (7/15)
# then the other 6 points -> 13/15
##################################################

##################################################
## globals ## (yeah, yeah, fuck off!)
##################################################

bg=None  # this capsules the abstract board
nconn = None # teh network-connection
reverse_colors = False

##################################################

def paint_background():
    """paints the board"""
    global screen
    
    screen.fill(pygame.color.Color('black'))
    h=screen.get_height()
    w=screen.get_width()
    boardcolor = pygame.color.Color('brown')

    # untere seite
    for i in range(3):
        pygame.draw.aalines(screen, boardcolor, True,
                            [((w/15)*(2*i), h),
                             ((w/15)*(2*i+1), h),
                             ((w/30)*(4*i+1), h-w/3)])
        pygame.draw.polygon(screen, boardcolor,
                            [((w/15)*(2*i+1), h),
                             ((w/15)*(2*i+2), h),
                             ((w/30)*(4*i+3), h-w/3)])
    for i in range(3,6):
        pygame.draw.aalines(screen, boardcolor, True,
                            [((w/15)*(2*i+1), h),
                             ((w/15)*(2*i+2), h),
                             ((w/30)*(4*i+3), h-w/3)])
        pygame.draw.polygon(screen, boardcolor,
                            [((w/15)*(2*i+2), h),
                             ((w/15)*(2*i+3), h),
                             ((w/30)*(4*i+5), h-w/3)])

    # obere seite
    for i in range(3):
        pygame.draw.polygon(screen, boardcolor,
                            [((w/15)*(2*i), 0),
                             ((w/15)*(2*i+1), 0),
                             ((w/30)*(4*i+1), w/3)])
        pygame.draw.aalines(screen, boardcolor, True,
                            [((w/15)*(2*i+1), 0),
                             ((w/15)*(2*i+2), 0),
                             ((w/30)*(4*i+3), w/3)])

    for i in range(3,6):
        pygame.draw.polygon(screen, boardcolor,
                            [((w/15)*(2*i+1), 0),
                             ((w/15)*(2*i+2), 0),
                             ((w/30)*(4*i+3), w/3)])
        pygame.draw.aalines(screen, boardcolor, True,
                            [((w/15)*(2*i+2), 0),
                             ((w/15)*(2*i+3), 0),
                             ((w/30)*(4*i+5), w/3)])

    pygame.draw.polygon(screen, boardcolor,
                        [((w/15)*6, 0), ((w/15)*6, h),
                         ((w/15)*7, h), ((w/15)*7, 0)])

def paint_box_npos(color, npos):
    """paints a box in color 'color' around point 'npos'"""
    h=screen.get_height()
    w=screen.get_width()

    npos = min(24,npos)

    xpos = npos - 12
    xpos_inverse = 11 - npos

    if (npos < 6):     x=(w/30) * (2*xpos_inverse + 2)
    elif (npos < 12):  x=(w/30) * (2*xpos_inverse)
    elif (npos < 18):  x=(w/30) * (2*xpos)
    else:              x=(w/30) * (2*xpos + 2)

    if (npos < 12):
        pygame.draw.aalines(screen, color, True,
                            [(x, 0), (x, w/3), (x+w/15, w/3), (x+w/15, 0)])
    else:
        pygame.draw.aalines(screen, color, True,
                            [(x, w), (x, h-w/3), (x+w/15, h-w/3), (x+w/15, w)])

def paint_piece_xy(bw, pos):
    """bw: color of the piece. black/white:True/False
    pos: (x,y) in pixels"""

    ### TODO remove ###
    #if turn: bw=not bw
    ###################

    bw = bw ^ reverse_colors
    
    colorwhite=pygame.color.Color('green')
    colorblack=pygame.color.Color('black')
    x,y = pos
    w=screen.get_width()
    if bw:
        pygame.draw.circle(screen, colorblack, (x,y), w/30, 0) # width=w/30?
        pygame.draw.circle(screen, colorwhite, (x,y), w/30, 1)
    else:
        pygame.draw.circle(screen, colorwhite, (x,y), w/30-1, 0)
        pygame.draw.circle(screen, colorblack, (x,y), w/30, 1)

def get_piece_barpos(bw, nth):
    """bw: 0/1 = white/black
    nth: the nth piece on the point
    returns: the (x,y) to where to paint a piece"""
    w=screen.get_width()
    h=screen.get_height()

    x=(w/30) * 13

    if (nth < 5):
        dist_to_border = (w/30) * (2*nth + 1)
    elif (nth < 9):
        dist_to_border = (w/30) * (2*(nth-5) + 2)
    elif (nth < 12):
        dist_to_border = (w/30) * (2*(nth-9) + 3)
    elif (nth < 14):
        dist_to_border = (w/30) * (2*(nth-12) + 4)
    else:
        dist_to_border = (w/30) * 5

    dist_to_border = (w/30)* 10 - dist_to_border

    if (bw):  y=dist_to_border
    else:         y=h - dist_to_border
    
    return (x,y)

def get_piece_outpos(bw, nth):
    """bw: 0/1 = white/black?
    nth: the nth piece on the point
    returns: the (x,y) to where to paint a piece"""
    w=screen.get_width()
    h=screen.get_height()

    x=(w/30) * 28

    if (nth < 5):
        dist_to_border = (w/30) * (2*nth + 1)
    elif (nth < 9):
        dist_to_border = (w/30) * (2*(nth-5) + 2)
    elif (nth < 12):
        dist_to_border = (w/30) * (2*(nth-9) + 3)
    elif (nth < 14):
        dist_to_border = (w/30) * (2*(nth-12) + 4)
    else:
        dist_to_border = (w/30) * 5

    if (bw):  y=dist_to_border
    else:         y=h - dist_to_border
    
    return (x,y)


def get_piece_npos(npos, nth):
    """npos: position on which the piece stands
       nth: the nth piece on the point
    returns: the (x,y) to where to paint a piece"""
    w=screen.get_width()
    h=screen.get_height()
    xpos = npos - 12
    xpos_inverse = 11 - npos

    if (npos < 6):   x=(w/30) * (2*xpos_inverse + 3)  # upper right
    elif (npos < 12):  x=(w/30) * (2*xpos_inverse + 1)  # upper left
    elif (npos < 18):  x=(w/30) * (2*xpos + 1)          # lower left
    else:              x=(w/30) * (2*xpos + 3)          # lower right

    if (nth < 5):
        dist_to_border = (w/30) * (2*nth + 1)
    elif (nth < 9):
        dist_to_border = (w/30) * (2*(nth-5) + 2)
    elif (nth < 12):
        dist_to_border = (w/30) * (2*(nth-9) + 3)
    elif (nth < 14):
        dist_to_border = (w/30) * (2*(nth-12) + 4)
    else:
        dist_to_border = (w/30) * 5

    if (npos < 12):    y=dist_to_border
    else:              y=h - dist_to_border
    
    return (x,y)

def anim_pointlist(fro, to, n):
    """fro: (x,y) from which to move
    to: (x,y) to which to move
    n: how many stops on the line
    returns: list of (x,y)s on the line"""
    to_x, to_y = to
    fro_x, fro_y = fro
    dist_x, dist_y = (to_x - fro_x, to_y - fro_y)
    return ((dist_x *i / n + fro_x, dist_y *i / n + fro_y) for i in xrange(n+1))

def display_turn(turn):
    col = turn^reverse_colors
    h=screen.get_height()
    w=screen.get_width()
    rect=pygame.Rect( ((w/15)*14, h/2-10), (w/15, 20))
    font=pygame.sysfont.SysFont('monospace', 14)
    pygame.draw.rect(screen, pygame.Color('white') if col else pygame.Color('green'), rect, 1 if col else 0)
    surface=font.render('Oppnt' if turn else 'You', True, pygame.Color('white') if col else pygame.Color('black'))
    screen.blit(surface, (rect.x, rect.y))

def display_text(text):
    h=screen.get_height()
    w=screen.get_width()
    rect=pygame.Rect( ((w/15)*8, h/2-10), ((w/15)*5, 20))
    font=pygame.sysfont.SysFont('monospace', 14)
    fgcolor=pygame.Color('white')
    bgcolor=pygame.Color('black')

    pips = (reduce(lambda x,y: x+y, ((24-a)*b for (a,b) in bg.position[0]))+
            bg.position[2][0]*25,
            reduce(lambda x,y: x+y, ((a+1)*b for (a,b) in bg.position[1]))+
            bg.position[2][1]*25)

    text = [ "Menu: [M]   Pips: %s/%s"%pips, text ]

    y=rect.y
    for t in text:
        surface=font.render(t, True, fgcolor, bgcolor)
        screen.blit(surface, (rect.x, y))
        y+=font.get_height()
        
def paintposition(pos, anim=2):
    """paints the pieces to the board
    pos: the position to paint
    anim=0/1 (white/black) for being used by the animation of pieces."""

    # white pieces
    painted = 0
    for (npos, n) in pos[0]:
        for x in range(n):
            paint_piece_xy(False, get_piece_npos(npos, x))
            painted+=1

    for x in range(pos[2][0]): # bar white
        paint_piece_xy(False, get_piece_barpos(False, x))
        painted += 1

    if (anim==0): m=14
    else: m=15
            
    for x in range(m-painted):  # pieces out
        paint_piece_xy(False, get_piece_outpos(False, x))
        
    # black pieces
    painted = 0
    for (npos, n) in pos[1]:
        for x in range(n):
            paint_piece_xy(True, get_piece_npos(npos, x))
            painted+=1

    for x in range(pos[2][1]): # bar black
        paint_piece_xy(True, get_piece_barpos(True, x))
        painted += 1

    if (anim==1): m=14
    else: m=15

    for x in range(m-painted):  # pieces out
        paint_piece_xy(True, get_piece_outpos(True, x))

def animatemove(pos, bw, fro, to):
    """animate a move
    pos: the position on which to animate
    bw: 0/1: white/blacl
    fro: point from
    to: point to"""

    #    paint_background()
    #   paintposition(pos)
    #   pygame.display.update()

    if (to<0 or to>23 or fro<0 or fro>23):
        return
    
    dpos = [dict(pos[0]), dict(pos[1]), pos[2]]
    dpos[bw][fro]-=1
    pos = [dpos[0].items(), dpos[1].items(), pos[2]]
    animpoints=anim_pointlist(get_piece_npos(fro, dpos[bw].setdefault(fro,0)), get_piece_npos(to, dpos[bw].setdefault(to,0)), 10)
    
    for (x,y) in animpoints:
        time.sleep(.05)
        paint_background()
        paintposition(pos, anim=bw)
        paint_piece_xy(bw, (x,y))
        pygame.display.update()

def paint_dice(avail, used=[]):
    """dice: two lists: available dice, used dice"""
    h=screen.get_height()
    w=screen.get_width()
    font=pygame.sysfont.SysFont('monospace', 40)

    dice = [(x, 'green') for x in avail] + [(x, 'red') for x in used]

    upper=h/2 - w/30
    lower=h/2 + w/30

    x = w/30
    for (num, color) in dice:
        rect = pygame.Rect( (x, upper), (w/15, w/15))
        pygame.draw.rect(screen, pygame.Color(color), rect, 1)
        surface=font.render('%s'%num, True, pygame.Color(color))
        screen.blit(surface, (rect.x, rect.y))
        x+=w/12

def translate_mouse_pos(pos):
    h=screen.get_height()
    w=screen.get_width()

    (x,y) = pos
    field = x/(w/15)
    if ( y< 5*(w/15) ):  # upper half
        if (field == 6): # bar
            point = -1
        elif (field < 6): # left side
            point = 11 - field
        elif (field < 13): # right side
            point = 12 - field
        else:  # out
            point = 24
            
        return ('point', point)

    elif ( y > h-5*(w/15) ): # lower half
        if (field == 6): # bar
            point = -1
        elif (field < 6): # left side
            point = 12 + field
        elif (field < 13): # right side
            point = 11 + field
        else:  # out
            point = 24

        return ('point', point)

    else:  # middle
        return ('middle',)

def do_roll(init, network_wait):
    """init: initiator?"""
    global nconn

    if (init):
        nconn.send("ROLL")
        r=roll.Roll('initiator')
        nconn.send(r.commitment)
        network_wait()
        chosenthrow = int(nconn.readline())
        r.chosenthrow = chosenthrow
        nconn.send(r.shuffle)

    else:
        network_wait()
        commitment = nconn.readline()
        r=roll.Roll('participant', commitment)
        nconn.send(r.chosenthrow)
        network_wait()
        shuffle = nconn.readline()
        r.set_shuffle(shuffle)

    sound.playsound('sounds/roll.wav')
    return r.get_throw()
    

# states:
# 'roll': click middle to roll
# 'choosepiece': move mouse to choose a piece to move
# 'movepiece': choose a point to move the piece or cancel by clicking on the piece

def error_window(msg):
    global screen
    mopgi.messagebox.MessageBox(screen, msg)
    nconn.send(QUIT)
    exit(1)
    
def gameloop(isserver):
    """the game.
    isserver: to distinguish between the partners. 
    important to find out who initiates the first roll"""

    def paint_everything():
        paint_background()
        if (throw != None):
            paint_dice(throw, used)
        paintposition(position)
        if (turn != None):
            display_turn(turn)
        display_text("")
        pygame.display.update()

    def common_keys(event):
        global reverse_colors
        if event.type == KEYDOWN:
            if event.key == K_f:  # fullscreen
                pygame.display.toggle_fullscreen()
                
            elif event.key == K_m:
                ingamemenu.menu(screen)

            elif event.key == K_r:
                reverse_colors = not reverse_colors

            paint_everything()

    def network_wait():
        while (not nconn.line_ready.is_set()):
            event = pygame.event.wait()
            common_keys(event)

    global turn, reverse_colors, bg
    old_trpos = None
    turn = isserver
    move = []
    throw = []
    used = []
    position = bg.position

    paint_background()
    paintposition(position)
    display_turn(turn)
    pygame.display.update()

    # who begins?
    throw = (0,0)   # invalid throw, but lhs == rhs
    while (throw[0] == throw[1]):
        if (not isserver):
            throw = do_roll(True, network_wait)
            used=[]
        else:
            network_wait()
            line = nconn.readline()
            if (line != "ROLL"):
                error_window(["protocol error", "expected ROLL got:", line])
                exit(1)
            throw = do_roll(False, network_wait)
            used = []
        print("rolled %s" % str(throw))

    if ((throw[0] > throw[1] and isserver) or
        (throw[1] > throw[0] and not isserver)):  # throw[0] is for the server
        turn=False
        state = 'choosepiece'
    else:
        turn=True
        state = 'waitforopponent'

    paint_everything()

    oldstate=state
    print("newstate = %s" % state)
          
    while True:
        if (oldstate != state):
            oldstate = state
            print("newstate = %s" % state)
            
        event = pygame.event.wait()
      
        if event.type == QUIT:
            sys.exit(0)

        elif event.type == USEREVENT:     # probably network-induced?
            if (state == 'opponentroll'):
                if (nconn.line_ready.is_set()):
                    line = nconn.readline()
                    if (line!='ROLL'):
                        error_window(['protocol error', 'expected ROLL got:', line])
                    used = []
                    throw = do_roll(False, network_wait)
                    if (throw[0] == throw[1]):
                        throw=[throw[0]]*4
                    state = 'waitforopponent'
                    paint_everything()
                    display_text('moving...')
                    
            if (state == 'waitforopponent'):
                if (nconn.line_ready.is_set()):
                    line = nconn.readline()
                    if (line!='MOVE'):
                        error_window(['protocol error', 'expected MOVE got:', line])
                    network_wait()
                    moves = nconn.readline()
                    opposition = bg.turnposition(position)
                    for m in moves.split(":"):
                        print("throw %s, used %s" %(str(throw), str(used)))
                        if (len(throw) == 0 or bg.possible_moves(opposition, throw) == False):
                            # no more moves possible
                            if (m != 'DONE'):
                                error_window(['opponent', "move not terminated"])
                        else:
                            (npos, n) = [int(x) for x in m.split("/")]
                            print("opponent-move: %s/%s" % (npos, n))
                            opposition = bg.do_one_move(opposition, npos, n)
                            if (opposition == False):
                                error_window(["opponent", "invalid move"])
                            paint_everything()
                            animatemove(position, turn, 23-npos, 23-npos-n)
                            sound.playsound('sounds/move.wav')
                            throw.remove(n)
                            used.append(n)
                            position = bg.turnposition(opposition)
                            paint_everything()

                    if (bg.possible_moves(opposition, throw) != False):
                        error_window("opponent didn't use all possible moves")

                    if (reduce(lambda x,y: x+y, (c for (p, c) in (opposition[0]))) + opposition[2][0] == 0):  # no pieces on board / win!
                        mopgi.messagebox.MessageBox(screen, "YOU LOSE!")
                        paint_everything()
                        break

                            
                    bg.position = position
                    turn = not turn
                    state='roll'
                    paint_everything()
                        
        elif event.type == MOUSEBUTTONUP:
            if (state == 'roll' and translate_mouse_pos(event.pos) == ('middle',)):
                throw = do_roll(True, network_wait)
                if (throw[0] == throw[1]):
                    throw=[throw[0]]*4
                used = []
                position = bg.position
                paint_everything()
                #print turn, bg.possible_moves(position, throw)
                if (bg.possible_moves(position, throw) == False):
                    mopgi.messagebox.MessageBox(screen, "No moves possible")
                    paint_everything()

                    nconn.send("MOVE")                                        
                    nconn.send("DONE")
                    move=[]
                    turn=not turn
                    state = 'opponentroll'
                    paint_everything()
                    display_text('rolling...')

                else:
                    state = 'choosepiece'
                
            elif (state == 'choosepiece'):
                trpos = translate_mouse_pos(event.pos)
                if (trpos[0] != 'point'):
                    continue
                possible = False
                for n in throw:
                    if (bg.do_one_move(position, trpos[1], n) != False):
                        possible=True
                if (possible):
                    chosenpiece=trpos[1]
                    print("chosenpiece %s" % chosenpiece)
                    paint_box_npos(pygame.Color('red'), chosenpiece)
                    state='movepiece'

            elif (state == 'movepiece'):
                trpos = translate_mouse_pos(event.pos)
                if (trpos[0] == 'point' and trpos[1] == chosenpiece):  # abort state
                    state = 'choosepiece'
                    paint_everything()
                    
                if (trpos[0] == 'point' and (trpos[1]-chosenpiece in throw) and  # normal move
                    bg.do_one_move(position, chosenpiece, trpos[1]-chosenpiece) != False):
                    n = trpos[1] - chosenpiece
                    animatemove(position, 0, chosenpiece, chosenpiece+n)
                    position=bg.do_one_move(position, chosenpiece, n)
                    throw.remove(n)
                    used.append(n)
                    paint_everything()
                    move+=[(chosenpiece, n)]
                    sound.playsound('sounds/move.wav')
                    state = 'choosepiece'
                    #print turn, bg.possible_moves(position, throw)

                elif (trpos[0] == 'point' and (trpos[1]==24) and not (trpos[1]-chosenpiece in throw)):  # wasting move
                    if (reduce(lambda x,y:x+y, (c for (p, c) in position[0] if p<chosenpiece)) == 0): ## may do wasting move
                        n=trpos[1]-chosenpiece
                        highest = max(throw)
                        if (highest>n):
                            tmppos=bg.do_one_move(position, chosenpiece, highest)
                            if (tmppos!=False):
                                position=tmppos
                                throw.remove(highest)
                                used.append(highest)
                                move+=[(chosenpiece, highest)]
                                paint_everything()
                                sound.playsound('sounds/move.wav')
                                state = 'choosepiece'
                                #print turn, bg.possible_moves(position, throw)

                if (reduce(lambda x,y: x+y, (c for (p, c) in (position[0]))) + position[2][0] == 0):  # no pieces on board / win!
                    mopgi.messagebox.MessageBox(screen, "YOU WIN!")
                    paint_everything()
                    movestring=":".join(["%s/%s" % m for m in move]) + ":DONE"
                    nconn.send("MOVE")                                        
                    nconn.send(movestring)
                    break
                    
                if (len(throw) == 0 or bg.possible_moves(position, throw) == False):
                    if (len(throw) > 0):
                        mopgi.messagebox.MessageBox(screen, "No more moves possible")
                        paint_everything()

                    movestring=":".join(["%s/%s" % m for m in move]) + ":DONE"
                    nconn.send("MOVE")                                        
                    nconn.send(movestring)
                    move=[]
                    turn=not turn
                    state = 'opponentroll'
                    bg.position = position
                    paint_everything()
                    display_text('rolling...')

        elif event.type == MOUSEMOTION:
            if (state == 'choosepiece'):
                trpos = translate_mouse_pos(event.pos)
                if (old_trpos != trpos):
                    old_trpos = trpos
                    paint_everything()
                    if (trpos[0] == 'point'):
                        npos = trpos[1]
                        paint_box_npos(pygame.Color('white'), npos)
                        for n in throw:
                            if (bg.do_one_move(position, npos, n) != False):
                                paint_box_npos(pygame.Color('green'), npos+n)
                    
                    pygame.display.update()

        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:  # undo
                if (state == 'choosepiece' or state == 'movepiece'):
                    throw=throw+used
                    used = []
                    move = []
                    position = bg.position
                    paint_background()
                    paint_dice(throw, used)
                    paintposition(position)
                    display_turn(turn)
                    state = 'choosepiece'

            else:
                common_keys(event)
                    
        pygame.display.update()

def main():
    global nconn, bg
    bg=bggame.BgGame()
    paint_background()
    (isserver, address) = menu.mainmenu(screen)
    if (isserver):
        paint_background()
        display_text("waiting...")
        pygame.display.update()
        nconn = network.NetworkConnection()
        nconn.listen()
        
    else:
        # mopgi.MessageBox(screen, "Connecting...", "Cancel")
        paint_background()
        display_text("connecting...")
        pygame.display.update()
        nconn = network.NetworkConnection()
        nconn.connect((address, network.STDPORT))

    gameloop(isserver)

if __name__ == '__main__':
    pygame.init()
    (SCREENRES_SX, SCREENRES_SY) = configuration.config['screenres'].split("x")
    screen=pygame.display.set_mode((int(SCREENRES_SX), int(SCREENRES_SY)))
    pygame.display.set_caption('SHLOC - Multiplayer Backgammon')

    main()
    