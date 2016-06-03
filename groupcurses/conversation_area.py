import uuid
import time
from datetime import datetime
import urwid

class ConversationArea(urwid.Filler):
    def __init__(self, api):
        self.api = api
        self.conversation_list = ConversationList(api)
        self.message_area = ConversationMessageArea()
        self.column_wrapper = ConversationColumns(self.conversation_list, self.message_area)
        super().__init__(self.column_wrapper, valign='top', height=('relative', 100))

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key is not 'enter':
            return key
        else:
            self.display_selected_conversation()

    def update_conversation_list(self):
        groups = self.api.get('groups')
        direct_messages = self.api.get('chats')
        if direct_messages is not None:
            for message in direct_messages:
                other_user = message['other_user']
                other_user_id = other_user['id']
                other_user_name = other_user['name']
                self.conversation_list.add_conversation(
                    other_user_id,
                    other_user_name,
                    'direct_message'
                )
        if groups is not None:
            for group in groups:
                group_id = group['id']
                group_name = group['name']
                self.conversation_list.add_conversation(group_id, group_name, 'group')

    def display_selected_conversation(self):
        conversation = self.conversation_list.get_focused_conversation()
        if conversation is not None:
            conversation.get_messages()
            self.message_area.clear()
            for message in conversation.messages:
                self.message_area.append(message.get_widget())
            self.message_area.messages.set_focus(len(conversation.messages) - 1)

class ConversationColumns(urwid.Columns):
    def __init__(self, conversation_list, message_area):
        self.conversation_list_wrapper = urwid.LineBox(conversation_list)
        self.message_area_wrapper = urwid.LineBox(message_area)
        super().__init__(
            [(20, self.conversation_list_wrapper), self.message_area_wrapper],
            box_columns=[0, 1]
        )

class ConversationList(urwid.ListBox):
    def __init__(self, api):
        self.api = api
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
            conversation = Conversation(self.api, cid, name, conversation_type)
            conversation_wrapper = urwid.AttrMap(conversation, None, 'highlight')
            self.list_index.append(conversation_index_entry)
            self.list.append(conversation_wrapper)

class Conversation(urwid.Text):
    def __init__(self, api, cid, name, conversation_type):
        self.api = api
        self.cid = cid
        self.name = name
        self.conversation_type = conversation_type
        self.messages_index = []
        self.messages = []
        self.get_messages()
        super().__init__(name)
    def selectable(self):
        return True
    def keypress(self, size, key):
        return key
    def get_messages(self):
        if self.conversation_type == 'direct_message':
            messages = self.api.get(
                'direct_messages',
                {'other_user_id': self.cid}
            )['direct_messages']
        elif self.conversation_type == 'group':
            messages = self.api.get('groups/' + self.cid + '/messages')['messages']
        messages.reverse()
        for message in messages:
            if not any(c == {'mid': message['source_guid']} for c in self.messages_index):
                sender = message['name']
                date = datetime.fromtimestamp(int(message['created_at'])).strftime("%H:%M:%S")
                text = message['text']
                mid = message['source_guid']
                self.append_message(mid, sender, date, text)
    
    def send_message(self, message):
        source_guid = str(uuid.uuid1())
        date = time.strftime("%H:%M:%S")
        if self.conversation_type == 'direct_message':
            message_data = {
                'direct_message': {
                    'source_guid': source_guid,
                    'recipient_id': self.cid,
                    'text': message,
                }
            }
            if self.api.post('direct_messages', user_data=message_data):
                self.append_message(source_guid, 'me', date, message)
    
    def append_message(self, mid, sender, date, message):
        self.messages_index.append({'mid': mid})
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
        if message is not None:
            self.message = message
        else:
            self.message = ''
    def get_widget(self):
        message_widget = urwid.Text(self.message)
        date_widget = urwid.Text('(' + self.date + ')')
        sender_widget = urwid.Text(self.sender + ': ')
        sender_pile = urwid.Pile([sender_widget, date_widget])
        return urwid.Columns([('weight', 0.4, sender_pile), message_widget], dividechars=1)
