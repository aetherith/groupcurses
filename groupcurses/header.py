import urwid

class HeaderArea(urwid.Padding):
    def __init__(self):
        self.title = urwid.Text(u"i:Compose c:Browse n:New q:Quit ESC:Main Mode")
        super().__init__(urwid.AttrMap(self.title, 'statusbar'))


