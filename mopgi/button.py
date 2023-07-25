import mopgi
import label
import pygame
from pygame.locals import *

class Button(label.Label):
    def __init__(self, parent, rect, text, action):
        label.Label.__init__(self, parent, rect, text)
        self.action = action
        self.have_focus = False
        self.mouse_hover = False

    def onmouseenter(self):
        self.mouse_hover=True
        self.parent.update()
        self.parent.gen_event()

    def onmouseleave(self):
        self.mouse_hover=False
        self.parent.update()
        self.parent.gen_event()

    def onmousebuttonup(self, pos, buttons):
        self.action()
        self.parent.update()
        self.parent.gen_event()

    def onkeydown(self, unicode, key, mod):
        if (key==K_SPACE or key == K_RETURN):
            self.action()
        self.parent.update()
        self.parent.gen_event()

    def paint(self, screen):
        if (self.mouse_hover):
            pygame.draw.rect(screen, self.fgcolor, self.rect)
            surface=self.font.render(self.text, True, self.bgcolor)
            screen.blit(surface, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, self.bgcolor, self.rect)
            if (self.have_focus):
                pygame.draw.rect(screen, self.fgcolor, self.rect, 2)
            else:
                pygame.draw.rect(screen, self.fgcolor, self.rect, 1)
                
            surface=self.font.render(self.text, True, self.fgcolor)
            screen.blit(surface, (self.rect.x, self.rect.y))

    def setfocus(self, have_focus):
        self.have_focus = have_focus
        self.parent.update()
        self.parent.gen_event()