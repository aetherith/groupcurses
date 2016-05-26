#!/usr/bin/env python3
# encoding: utf-8
import time
import threading

import urwid

from api import API
from configuration import Configuration
from conversation_area import ConversationArea
from input_area import InputArea

class GroupCursesApp(urwid.MainLoop):
    def __init__(self):
        urwid.set_encoding("UTF-8")
        self.POLL_INTERVAL = 5
        try:
            self.configuration = Configuration()
        except Exception as e:
            print(e)
            raise urwid.ExitMainLoop()
        self.api = API(self.configuration.api_key)
        self.header_area = HeaderArea()
        self.input_area = InputArea() 
        self.conversation_area = ConversationArea(self.api)
        self.main_screen = urwid.Frame(self.conversation_area, header=self.header_area, footer=self.input_area)
        self.palette = [
                ('statusbar', 'black', 'light gray'),
                ('input_mode', 'white', 'dark red'),
                ('normal_mode', 'black', 'dark green'),
                ('highlight', 'black', 'light gray'),
                ]
       
        self.register_signal_emitters()
        self.connect_signal_handlers()
        super().__init__(self.main_screen, self.palette, unhandled_input=self.navigation_handler)
        
        # Initialize the conversation list refresh loop.
        # This should be done before trying to refresh the message area to avoid
        # a wait between first render and messages showing up.
        self.conversation_list_refresh_handler(None, None)
        
        # Initialize the refresh message area refresh loop.
        self.conversation_messages_refresh_handler(None, None)

    def register_signal_emitters(self):
        urwid.register_signal(API, 'show-status-message')
        urwid.register_signal(InputArea, 'message-send')

    def connect_signal_handlers(self):
        urwid.connect_signal(self.api, 'show-status-message', self.show_status_message_handler)
        urwid.connect_signal(self.input_area, 'message-send', self.send_message_handler)
  
    def conversation_list_refresh_handler(self, main_loop, user_data):
        self.conversation_area.update_conversation_list()
        self.set_alarm_in(self.POLL_INTERVAL, self.conversation_list_refresh_handler)

    def conversation_messages_refresh_handler(self, main_loop, user_data):
        self.conversation_area.display_selected_conversation()
        self.set_alarm_in(self.POLL_INTERVAL, self.conversation_messages_refresh_handler)
    
    def navigation_handler(self, key):
        if key is 'q':
            raise urwid.ExitMainLoop()
        if key is 'i':
            self.input_area.set_mode('compose')
            self.main_screen.focus_position = 'footer'
        if key is 'c':
            self.main_screen.focus_position = 'body'
            self.conversation_area.focus_position = 0
        if key is 'esc':
            self.input_area.set_mode('normal')
            self.main_screen.focus_position = 'body'

    def send_message_handler(self, message):
        self.input_area.input_field.set_edit_text(u"")
        current_conversation = self.conversation_area.conversation_list.get_focused_conversation()
        date = time.strftime("%H:%M:%S")
        current_conversation.append_message('me', date, message)
        self.conversation_area.display_selected_conversation()

    def show_status_message_handler(self, message, severity='info'):
        self.input_area.set_message(message, severity)



    def get_conversation_messages_handler(self, conversation):
        if conversation.type == 'chat':
            pass
        elif conversation.type == 'group':
            pass

class HeaderArea(urwid.Padding):
    def __init__(self):
        self.title = urwid.Text(u"i:Compose c:Browse n:New q:Quit ESC:Main Mode")
        super().__init__(urwid.AttrMap(self.title, 'statusbar'))

if __name__ == "__main__":
    App = GroupCursesApp()
    App.run()
