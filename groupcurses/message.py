from urwid import Text, Pile, Columns

class Message():
    def __init__(self, sender, date, message):
        self.sender = sender
        self.date = date
        if message is not None:
            self.message = message
        else:
            self.message = ''
    def get_widget(self):
        message_widget = Text(self.message)
        date_widget = Text('(' + self.date + ')')
        sender_widget = Text(self.sender + ': ')
        sender_pile = Pile([sender_widget, date_widget])
        return Columns([('weight', 0.4, sender_pile), message_widget], dividechars=1)
