#!/usr/bin/env python3
# encoding: utf-8
"""
A terminal based application to interact with the GroupMe API.
"""
import urwid

from groupcurses.groupme_api import GroupMeAPI
from groupcurses.configuration import Configuration
from groupcurses.header import HeaderArea
from groupcurses.conversation_area import ConversationArea
from groupcurses.input_area import InputArea

class GroupCursesApp(urwid.MainLoop):
    """
    A terminal based application to interact with multiple chat APIs.
    """
    def __init__(self):
        urwid.set_encoding("UTF-8")
        self.POLL_INTERVAL = 10
        try:
            self.configuration = Configuration()
        except Exception as error:
            print(error)
            raise urwid.ExitMainLoop()
        self.apis = {}
        if 'groupme' in self.configuration.config['general']['interfaces']:
            self.apis['groupme'] = GroupMeAPI(self.configuration.config['groupme']['api_key'])
        self.header_area = HeaderArea()
        self.input_area = InputArea()
        self.conversation_area = ConversationArea(self.apis)
        self.main_screen = urwid.Frame(
            self.conversation_area,
            header=self.header_area,
            footer=self.input_area
        )
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
        """
        Inform urwid of which classes will be sending specific signals.
        """
        if 'groupme' in self.configuration.config['general']['interfaces']:
            urwid.register_signal(GroupMeAPI, 'show-status-message')
        urwid.register_signal(InputArea, 'message-send')

    def connect_signal_handlers(self):
        """
        Configure urwid to dispatch handlers when specific events fire.
        """
        if 'groupme' in self.configuration.config['general']['interfaces']:
            urwid.connect_signal(
                self.apis['groupme'],
                'show-status-message',
                self.show_status_message_handler
            )
        urwid.connect_signal(
            self.input_area,
            'message-send',
            self.send_message_handler
        )

    def conversation_list_refresh_handler(self, main_loop, user_data):
        """
        Update conversation list and set trigger for next update.
        """
        self.conversation_area.update_conversation_list()
        self.set_alarm_in(self.POLL_INTERVAL, self.conversation_list_refresh_handler)

    def conversation_messages_refresh_handler(self, main_loop, user_data):
        """
        Update current conversation's message list and set trigger to poll again.
        """
        self.conversation_area.display_selected_conversation()
        self.set_alarm_in(self.POLL_INTERVAL, self.conversation_messages_refresh_handler)

    def navigation_handler(self, key):
        """
        Handle any keyboard input not already handled by another widget.

        This is where we switch focus between our different input areas and
        summon new dialogs when required.
        """
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
            self.show_status_message_handler(u"")
            self.main_screen.focus_position = 'body'

    def send_message_handler(self, message):
        """
        Handle grabbing the correct conversation API and sending message.
        """
        self.input_area.input_field.set_edit_text(u"")
        current_conversation = self.conversation_area.conversation_list.get_focused_conversation()
        current_conversation.send_message(message)
        self.conversation_area.display_selected_conversation()

    def show_status_message_handler(self, message, severity='info'):
        """
        Display a status message to the user in the flightline.

        This method will eventually be extended to include different message
        colors based on the severity of the message.
        """
        self.input_area.set_message(message, severity)

def main():
    """
    Default application instantiation.
    """
    app = GroupCursesApp()
    app.run()

if __name__ == "__main__":
    main()
