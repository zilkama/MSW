import button

class RadioButton(button.Button):
    def __init__(self, parent, rect, optiontext, ticked=False):
        button.Button.__init__(self, parent, rect, "", self.toggletick)
        self.ticked = ticked
        self.optiontext = optiontext
        self._maketext()

    def _maketext(self):
        self.text = "[%s] %s" % ("X" if self.ticked else "_", self.optiontext)
        self.parent.update()

    def toggletick(self):
        self.ticked = not self.ticked
        self._maketext()
        
