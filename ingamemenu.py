import mopgi
import pygame
import sys
import configuration

def cb_okbutton(pgi):
    pgi.end()

def cb_helpbutton(screen):
    mopgi.MessageBox(screen, """SHLOC-Multiplayer-Backgammon
* Some Hundred Lines Of Code *
written by Moritz Molle
--------------------------
default port 25093
--------------------------
[M] Menu         [R]  Reverse
[F] Fullscreen   [<-] Undo

To Unchoose a piece, click it again.
To roll, click in the middle of the board
(on the dice)
    """.split('\n'))

def menu(screen):
    def setres(res):
        if (res != None):
            configuration.config['screenres'] = res
        else:
            res = configuration.config['screenres']
        r1024x768.text = '[%s] 1024x768' % ('X' if res=='1024x768' else ' ')
        r800x600.text = '[%s] 800x600' % ('X' if res=='800x600' else ' ')
        r640x480.text = '[%s] 640x480' % ('X' if res=='640x480' else ' ')
        
    pgi = mopgi.PGI(screen, 400, 300)
    title = mopgi.Label(pgi, pygame.Rect(150, 10, 100, 20), "SHLOC-Multiplayer-Backgammon")

    r1024x768 = mopgi.Button(pgi, pygame.Rect(25, 40, 100, 20), "", lambda: setres("1024x768"))
    r800x600 = mopgi.Button(pgi, pygame.Rect(150, 40, 100, 20), "", lambda: setres("800x600"))
    r640x480 = mopgi.Button(pgi, pygame.Rect(275, 40, 100, 20), "", lambda: setres("640x480"))

    defservlabel = mopgi.Label(pgi, pygame.Rect(50, 70, 300, 20), "Defaultserver/Port")
    defservinput = mopgi.SimpleInput(pgi, pygame.Rect(50, 100, 300, 20))

    servermode = mopgi.RadioButton(pgi, pygame.Rect(50, 130, 300, 20), "Servermode")

    rbsound = mopgi.RadioButton(pgi, pygame.Rect(50, 160, 300, 20 ), "Sound", configuration.config['sound'])

    okbutton = mopgi.Button(pgi, pygame.Rect(50, 250, 100, 20), "Ok", lambda: cb_okbutton(pgi))
    helpbutton = mopgi.Button(pgi, pygame.Rect(250, 250, 100, 20), "Help", lambda: cb_helpbutton(screen))
    
    pgi.add_widget(title)
    pgi.add_widget(r1024x768)
    pgi.add_widget(r800x600)
    pgi.add_widget(r640x480)

    setres(None)

    defservinput.text = configuration.config['defaultserver']
    servermode.ticked = configuration.config['servermode']
    
    pgi.add_widget(defservlabel)
    pgi.add_widget(defservinput)
    pgi.add_widget(servermode)
    pgi.add_widget(rbsound)
    pgi.add_widget(okbutton)
    pgi.add_widget(helpbutton)
    pgi.run()

    configuration.config['defaultserver'] = defservinput.text
    configuration.config['servermode'] = servermode.ticked
    configuration.config['sound'] = rbsound.ticked

    return