import mopgi
import label
import button
import pygame

def MessageBox(screen, message, btn='OK'):
    def onokbutton():
        pgi.end()
        pgi.update()
        
    pgi = mopgi.PGI(screen, 400, 300)
    l = label.Label(pgi, pygame.Rect(10, 10, 380, 240), message)
    ok = button.Button(pgi, pygame.Rect(160, 260, 80, 20), btn, onokbutton)
    pgi.add_widget(l)
    pgi.add_widget(ok)
    pgi.update()
    pgi.gen_event()
    pgi.run()
    