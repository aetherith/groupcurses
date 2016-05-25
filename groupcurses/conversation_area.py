import time
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

    def update_conversation_list(self, groups, direct_messages):
        for message in direct_messages:
            other_user = message['other_user']
            other_user_id = other_user['id']
            other_user_name = other_user['name']
            self.conversation_list.add_conversation(other_user_id, other_user_name, 'direct_message')
        for group in groups:
            group_id = group['id']
            group_name = group['name']
            self.conversation_list.add_conversation(group_id, group_name, 'group')

    def display_selected_conversation(self):
        conversation = self.conversation_list.get_focused_conversation()
        if conversation is not None:
            self.message_area.clear()
            conversation.append_message('system', time.strftime("%H:%M:%S"), 'refresh')
            for message in conversation.messages:
                self.message_area.append(message.get_widget())

class ConversationColumns(urwid.Columns):
    def __init__(self, conversation_list, message_area):
        self.conversation_list_wrapper = urwid.LineBox(conversation_list)
        self.message_area_wrapper = urwid.LineBox(message_area)
        super().__init__([(20, self.conversation_list_wrapper), self.message_area_wrapper], box_columns=[0, 1])

class ConversationList(urwid.ListBox):
    def __init__(self):
        self.list = urwid.SimpleFocusListWalker([])
        self.list_index = []
        super().__init__(self.list)
    def get_focused_conversation(self):
        # Get the AttrMap wrapper of the focused element out of the tuple
        focused_element_wrapper = self.list.get_focus()[0]
        if focused_element_wrapper is not None:
            return focused_element_wrapper.original_widget
        else:
            return None
    def add_conversation(self, cid, name, conversation_type):
        conversation_index_entry = {
                'cid': cid,
                'name': name,
                'type': conversation_type
                }
        if not any(c == conversation_index_entry for c in self.list_index):
            conversation = Conversation(cid, name, conversation_type)
            conversation_wrapper = urwid.AttrMap(conversation, None, 'highlight')
            self.list_index.append(conversation_index_entry)
            self.list.append(conversation_wrapper)

class Conversation(urwid.Text):
    def __init__(self, cid, name, conversation_type):
        self.cid = cid
        self.name = name
        self.conversation_type = conversation_type
        self.messages = [Message('Jess', '12:30', 'Test'), Message('me', '12:31', 'Test2')]
        super().__init__(name)
    def selectable(self):
        return True
    def keypress(self, size, key):
        return key
    def append_message(self, sender, date, message):
        self.messages.append(Message(sender, date, message))

class ConversationMessageArea(urwid.ListBox):
    def __init__(self):
        self.messages = urwid.SimpleListWalker([])
        super().__init__(self.messages)
    def append(self, message):
        self.messages.append(message)
    def clear(self):
        self.messages.clear()

class Message():
    def __init__(self, sender, date, message):
        self.sender = sender
        self.date = date
        self.message = message
    def get_widget(self):
        message_widget = urwid.Text(self.message)
        sender_widget = urwid.Text('(' + self.date + ') ' + self.sender + ': ')
        return urwid.Columns([('pack', sender_widget), message_widget])
