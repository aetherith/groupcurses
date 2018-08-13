import uuid
import time
from datetime import datetime

import urwid

from groupcurses.message import Message

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
        messages = self.api.get_messages(self.conversation_type, self.cid)
        for message in messages:
            if not any(c == {'mid': message['source_guid']} for c in self.messages_index):
                sender = message['name']
                date = datetime.fromtimestamp(int(message['created_at'])).strftime("%H:%M:%S")
                text = message['text']
                mid = message['source_guid']
                self.append_message(mid, sender, date, text)
    
    def send_message(self, message):
        """
        Send a text message.

        TODO: Find a way to decouple the max message length.
        """
        source_guid = str(uuid.uuid1())
        date = time.strftime("%H:%M:%S")
        self.api.send_message(
            self.conversation_type,
            self.cid,
            source_guid,
            message[:1000]
        )
        if self.api.send_message(self.conversation_type, self.cid, source_guid, message):
            self.append_message(source_guid, 'me', date, message[:1000])
        if len(message) > 1000:
            self.send_message(message[1000:])
    
    def append_message(self, mid, sender, date, message):
        self.messages_index.append({'mid': mid})
        self.messages.append(Message(sender, date, message))
