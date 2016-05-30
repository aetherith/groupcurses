# GroupCurses

I've recently started using [GroupMe][groupme] a lot more to keep in contact
with a few people. Unfortunately, the existing commandline applications to
interact with their API either aren't my style or are written in a langauge
I'd have a hard time modifying. So instead, I built GroupCurses on top of 
[urwid][urwid] and [requests][requests] in Python3 in the hope of first getting
a stable connection to GroupMe and then branching out to try and interface with
other chap APIs. That way I don't have to pick which applicaiton to use, I can
chat with anyone.

# Installation

Should be as easy as a `pip install` but if that doesn't work, I'm building
against urwid v1.3.1 and requests v2.10.0 so you'll need access to those and
have them running in Python 3.5. This really is my first major Python project
so I haven't done a lot of testing for what versions of Python it works with.

# Use

The biggest thing is the vim like interface. Currently there are 3 modes for
the application which can be accessed using keybindings. The application starts
in Normal mode and can be returned there at any time by pressing `ESC`.

When in normal mode you can scroll through your available groups and direct
messages in the sidebar. Selecting a conversation will load the last 20 or so
messages and display them in the message area.

New messages can be composed by hitting `i` to enter Compose mode which shifts
focus to the textbox at the bottom of the application. Messages are sent when
you hit enter.

# Outstanding Tasks
* Create new direct messages
* Group messages - the whole workflow
* Emoji
* Improve the message sync methods so that they request only new messages.
* Improve the message area so that it supports scrolling better.

[groupme]: https://groupme.com
[urwid]: http://urwid.org/index.html
[requests]: http://docs.python-requests.org/en/master/
