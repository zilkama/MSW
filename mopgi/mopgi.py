import pygame
import sys
from pygame.locals import *

color_black=pygame.color.Color('black')
color_white=pygame.color.Color('white')

class Widget:
    def __init__(self, parent, rect):
        self.parent = parent
        self.rect = rect

    def paint(self):
        # has to be overloaded
        pass

    def onmousemotion(self, pos):
        # has to be overloaded
        pass

    def onmousebuttonup(self, pos, buttons):
        # has to be overloaded
        pass

    def onmouseenter(self):
        pass

    def onmouseleave(self):
        pass
    
    def onkeydown(self, unicode, key, mod):
        # has to be overloaded
        pass

    def setfocus(self, have_focus):
        # has to be overloaded
        pass
    
class PGI:    
    def __init__(self, screen, width=-1, height=-1, bgcolor=color_black, fgcolor=color_white, x=-1, y=-1):
        self.oldscreen = screen.copy()

        if (width == -1): width = screen.get_width()
        self.width = width
        if (height == -1): height = screen.get_height()
        self.height = height

        if (x==-1): self.x = (screen.get_width()-width) /2
        else:       self.x = x
        if (y==-1): self.y = (screen.get_height()-height) /2
        else:       self.y = y
        
        self.has_to_update = False
        self.mouse_in_widget = None

        self.widgets = []
        self.focus = -1
        self.screen = screen.subsurface(self.x, self.y, width, height)
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.clear()
        self.update()
        self.ended = False

    def innerpos(self, pos):
        return (pos[0]-self.x, pos[1]-self.y)

    def clear(self):
        self.screen.fill(self.bgcolor)
        pygame.draw.rect(self.screen, self.fgcolor,
                         pygame.Rect(0,0, self.screen.get_width(), self.screen.get_height()-1), 1)

    def add_widget(self, widget):
        self.widgets.append(widget)

    def paint(self):
        self.clear()
        for w in self.widgets:
            w.paint(self.screen)
        self.has_to_update = False
        pygame.display.update()

    def update(self):
        self.has_to_update = True

    def gen_event(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))

    def onmousemotion(self, pos):
        if (self.mouse_in_widget):
            if (not self.mouse_in_widget.rect.collidepoint(pos)):
                self.mouse_in_widget.onmouseleave()
                self.mouse_in_widget = None
                
        for w in self.widgets:
            if w.rect.collidepoint(pos):
                if (not self.mouse_in_widget):
                    self.mouse_in_widget = w
                    self.mouse_in_widget.onmouseenter()
                w.onmousemotion(pos)
                break

    def onmousebuttonup(self, pos, buttons):
        for w in self.widgets:
            if w.rect.collidepoint(pos):
                w.onmousebuttonup(pos, buttons)

    def onkeydown(self, unicode, key, mod):
        if (self.focus != -1):
            self.widgets[self.focus].onkeydown(unicode, key, mod)

    def rotate_focus(self):
        if (self.focus != -1):
            self.widgets[self.focus].setfocus(False)

        self.focus = (self.focus + 1) % len(self.widgets)
        self.widgets[self.focus].setfocus(True)

    def set_focus(self, widget):
        if (self.focus != -1):
            self.widgets[self.focus].setfocus(False)

        self.focus = self.widgets.index(widget)
        self.widgets[self.focus].setfocus(True)

    def run(self):
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == MOUSEBUTTONUP:
                self.onmousebuttonup(self.innerpos(event.pos), event.button)
            elif event.type == MOUSEMOTION:
                self.onmousemotion(self.innerpos(event.pos))
            elif event.type == KEYDOWN:
                if event.key == K_TAB:
                    self.rotate_focus()
                    self.update()
                else:
                    self.onkeydown(event.unicode, event.key, event.mod)
                        
            if self.has_to_update:
                self.paint()

            if self.ended:
                break
                
    def end(self):
        self.screen.blit(self.oldscreen, (0,0))
        self.ended = True
        self.update()
        self.gen_event()
      

if __name__=='__main__':
    import label
    import button
    import input

    pygame.init()
    screen=pygame.display.set_mode((640, 480))
    pygame.display.set_caption('mopgi-test')
    
    pgi = PGI(screen)
    pgi.add_widget(label.Label(pgi, pygame.Rect(10,10,100,30), ["hello, ","world!"]))
    pgi.add_widget(button.Button(pgi, pygame.Rect(20, 70, 100, 30), "Quit", lambda: sys.exit(0)))
    pgi.add_widget(input.SimpleInput(pgi, pygame.Rect(10, 120, 100, 20)))
    pgi.run()
    