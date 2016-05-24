import urwid

class ConversationArea(urwid.Filler):
    def __init__(self):
        self.conversation_list = ConversationList()
        self.message_area = ConversationMessageArea()
        self.column_wrapper = ConversationColumns(self.conversation_list, self.message_area)
        super().__init__(self.column_wrapper, valign='top', height=('relative', 100))

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key is not 'enter':
            return key
        else:
            self.display_selected_conversation()

    def request_conversations_update(self):
        urwid.emit_signal(self, 'get-conversations')
    
    def update_conversation_list(self, groups, direct_messages):
        for message in direct_messages:
            other_user = message['other_user']
            conversation = Conversation(other_user['name'], 'direct_message')
            conversation_wrapper = urwid.AttrMap(conversation, None, 'highlight')
            self.conversation_list.list.append(conversation_wrapper)
        for group in groups:
            group_name = group['name']
            conversation = Conversation(group_name, 'group')
            conversation_wrapper = urwid.AttrMap(conversation, None, 'highlight')
            self.conversation_list.list.append(conversation_wrapper)
    def display_selected_conversation(self):
        conversation = self.conversation_list.get_focused_conversation()
        self.message_area.clear()
        for message in conversation.messages:
            self.message_area.append(message)

class ConversationColumns(urwid.Columns):
    def __init__(self, conversation_list, message_area):
        self.conversation_list_wrapper = urwid.LineBox(conversation_list)
        self.message_area_wrapper = urwid.LineBox(message_area)
        super().__init__([(20, self.conversation_list_wrapper), self.message_area_wrapper], box_columns=[0, 1])

class ConversationList(urwid.ListBox):
    def __init__(self):
        self.list = urwid.SimpleFocusListWalker([])
        super().__init__(self.list)
    def get_focused_conversation(self):
        # Get index of the focused element out of the returned tuple
        focused_element_index = self.list.get_focus()[1]
        # Get the AttrMap that wraps our text.
        focused_element_wrapper = self.list[focused_element_index]
        focused_element = focused_element_wrapper.original_widget
        return focused_element

class Conversation(urwid.Text):
    def __init__(self, name, conversation_type):
        self.name = name
        self.conversation_type = conversation_type
        self.messages = [urwid.Text("I'm a Message")]
        super().__init__(name)
    def selectable(self):
        return True
    def keypress(self, size, key):
        return key

class ConversationMessageArea(urwid.ListBox):
    def __init__(self):
        self.messages = urwid.SimpleListWalker([urwid.Text(u"test message")])
        super().__init__(self.messages)
    def append(self, message):
        self.messages.append(message)
    def clear(self):
        self.messages.clear()

class Message():
    def __init__(self):
        pass
