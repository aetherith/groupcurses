import urwid

class InputArea(urwid.Pile):
    def __init__(self):
        self.mode = urwid.Text(u"")
        self.set_mode('normal')
        self.message = urwid.Text(u"> ")
        self.message_wrapper = urwid.Padding(urwid.AttrMap(self.message, 'statusbar'))
        self.status_line = urwid.Columns([('pack', self.mode), self.message_wrapper])
        self.input_field = urwid.Edit()
        super().__init__([self.status_line, self.input_field], focus_item=self.input_field)
    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key is not 'enter':
            return key
        else:
            message_text = self.input_field.get_edit_text()
            urwid.emit_signal(self, 'message-send', message_text)
    def set_mode(self, mode):
        if mode is 'normal':
            self.mode.set_text(('normal_mode', u"NORMAL "))
        elif mode is 'compose':
            self.mode.set_text(('input_mode', u"COMPOSE "))
    def set_message(self, message, severity):
        self.message.set_text(u"> " + message)
