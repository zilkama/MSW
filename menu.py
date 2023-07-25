import mopgi
import pygame
import sys
import configuration

def startgame(pgi):
    pgi.end()

def quitgame():
    sys.exit(0)

def mainmenu(screen):
    pgi = mopgi.PGI(screen, 400, 300)
    startgamebutton = mopgi.Button(pgi, pygame.Rect(50, 200, 100, 20),
                                   "Start Game", lambda: startgame(pgi))
    quitbutton = mopgi.Button(pgi, pygame.Rect(200, 200, 50, 20), "Quit", quitgame)
    serverbutton = mopgi.RadioButton(pgi, pygame.Rect(50, 150, 200, 20), "Server", configuration.config['servermode']!='False')
    label = mopgi.Label(pgi, pygame.Rect(50, 70, 200, 20), "Network Address / listening port")
    inputwidget = mopgi.SimpleInput(pgi, pygame.Rect(50, 100, 200, 20))

    inputwidget.text = (configuration.config['defaultserver'])
    
    pgi.add_widget(inputwidget)
    pgi.add_widget(serverbutton)
    pgi.add_widget(startgamebutton)
    pgi.add_widget(quitbutton)
    pgi.add_widget(label)
    pgi.run()

    return (serverbutton.ticked, inputwidget.text)
