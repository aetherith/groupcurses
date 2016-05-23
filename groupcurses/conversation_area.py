import urwid

class ConversationArea(urwid.Filler):
    def __init__(self):
        self.conversation_list = ConversationList()
        self.column2 = urwid.Filler(urwid.Text(u"column2"))
        self.column_wrapper = ConversationColumns(self.conversation_list, self.column2)
        super().__init__(self.column_wrapper, valign='top', height=('relative', 100))
    def request_conversations_update(self):
        urwid.emit_signal(self, 'get-conversations')
    def update_conversation_list(self, groups, direct_messages):
        for conversation in direct_messages:
            other_user = conversation['other_user']
            self.conversation_list.conversation_list.contents.append(urwid.Text(other_user['name']))

class ConversationColumns(urwid.Columns):
    def __init__(self, conversation_list, conversation_messages):
        self.conversation_list = conversation_list
        self.conversation_messages = conversation_messages
        super().__init__([(self.conversation_list, self.options(box_widget=True)), (self.conversation_messages, self.options(box_widget=True))])

class ConversationList(urwid.ListBox):
    def __init__(self):
        self.list = urwid.SimpleListWalker([urwid.Text(u"Test1")])
        self.list.contents.append(urwid.Text(u"Test"))
        super().__init__(self.list)

class Conversation():
    def __init__(self):
        pass

class ConversationMessageArea():
    def __init__(self):
        pass

class Message():
    def __init__(self):
        pass
