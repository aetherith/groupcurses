#!/usr/bin/env python3
# encoding: utf-8

import urwid

from api import API
from configuration import Configuration
from conversation_area import ConversationArea

class GroupCursesApp(urwid.MainLoop):
    def __init__(self):
        urwid.set_encoding("UTF-8")
        try:
            self.configuration = Configuration()
        except Exception as e:
            print(e)
            raise urwid.ExitMainLoop()
        self.api = API(self.configuration.api_key)
        self.header_area = HeaderArea()
        self.input_area = InputArea() 
        self.conversation_area = ConversationArea()
        self.main_screen = urwid.Frame(self.conversation_area, header=self.header_area, footer=self.input_area)
        
        self.register_signal_emitters()
        self.connect_signal_handlers()
        super().__init__(self.main_screen, unhandled_input=self.navigation_handler)
        self.conversation_area.request_conversations_update()

    def register_signal_emitters(self):
        urwid.register_signal(API, 'show-status-message')
        urwid.register_signal(InputArea, 'message-send')
        urwid.register_signal(ConversationArea, 'get-conversations')

    def connect_signal_handlers(self):
        urwid.connect_signal(self.api, 'show-status-message', self.show_status_message_handler)
        urwid.connect_signal(self.input_area, 'message-send', self.send_message_handler)
        urwid.connect_signal(self.conversation_area, 'get-conversations', self.get_conversations_handler)
    
    def navigation_handler(self, key):
        if key is 'q':
            raise urwid.ExitMainLoop()
        if key is 'i':
            self.main_screen.focus_position = 'footer'
        if key is 'esc':
            self.main_screen.focus_position = 'body'

    def send_message_handler(self, message):
        self.input_area.input_field.edit_text = u"Submitted - " + message

    def show_status_message_handler(self, message, severity='info'):
        self.input_area.status_line.set_text(message)

    def get_conversations_handler(self):
        groups = self.api.get('groups')
        direct_messages = self.api.get('chats')
        self.conversation_area.update_conversation_list(groups, direct_messages)

class HeaderArea(urwid.Padding):
    def __init__(self):
        self.title = urwid.Text(u"i:Compose c:Browse n:New q:Quit ESC:Main Mode")
        super().__init__(self.title)

class InputArea(urwid.Pile):
    def __init__(self):
        self.status_line = urwid.Text(u"Statusbar")
        self.input_field = urwid.Edit()
        super().__init__([self.status_line, self.input_field], focus_item=self.input_field)
    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key is not 'enter':
            return key
        else:
            message_text = self.input_field.get_edit_text()
            urwid.emit_signal(self, 'message-send', message_text)

if __name__ == "__main__":
    App = GroupCursesApp()
    App.run()
