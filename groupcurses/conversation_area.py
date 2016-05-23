import urwid

class ConversationArea(urwid.Filler):
    def __init__(self):
        self.column1 = urwid.Text(u"column1")
        self.column2 = urwid.Text(u"column2")
        self.column_wrapper = urwid.Columns([self.column1, self.column2])
        super().__init__(self.column_wrapper)
    def request_conversations_update(self):
        urwid.emit_signal(self, 'get-conversations')
    def update_conversation_list(self, groups, direct_messages):
        self.column1.set_text(direct_messages[0]['other_user']['name'])

class ConversationList():
    def __init__(self):
        pass

class Conversation():
    def __init__(self):
        pass

class ConversationMessageArea():
    def __init__(self):
        pass

class Message():
    def __init__(self):
        pass
