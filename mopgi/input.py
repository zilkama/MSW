import mopgi
import pygame
from pygame.locals import *

class SimpleInput(mopgi.Widget):
    def __init__(self, parent, rect):
        mopgi.Widget.__init__(self, parent, rect)
        self.text = ''
        self.setfont(pygame.sysfont.SysFont('monospace', 14))
        self.fgcolor = parent.fgcolor
        self.bgcolor = parent.bgcolor
        self.have_focus = False

    def setfgcolor(self, color):
        self.fgcolor = color
        self.parent.update()

    def setbgcolor(self, color):
        self.bgcolor = color
        self.parent.update()

    def setfont(self, font):
        self.font = font

    def paint(self, screen):
        pygame.draw.rect(screen, self.bgcolor, self.rect)
        if (self.have_focus):
            rendertext=self.text+"_"
            pygame.draw.rect(screen, self.fgcolor, self.rect, 2)
        else:
            rendertext = self.text
            pygame.draw.rect(screen, self.fgcolor, self.rect, 1)
            
        surface=self.font.render(rendertext, True, self.fgcolor)
        screen.blit(surface, (self.rect.x, self.rect.y))

    def setfocus(self, have_focus):
        self.have_focus = have_focus
        self.parent.update()

    def onkeydown(self, unicode, key, mod):
        if (key == K_BACKSPACE):
            self.text = self.text[:-1]
            self.parent.update()
        else:
            self.text += unicode
            self.parent.update()

    def onmousebuttonup(self, pos, buttons):
        self.parent.set_focus(self)
        