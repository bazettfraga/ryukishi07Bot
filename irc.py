from irc_class import *
import os 
import random

channel = "#07Wonderland"
server = "irc.swiftirc.net"
nickname = "Ryukishi07"


irc = IRC()
irc.connect(server, channel, nickname)

while 1:
    text = irc.get_text()
    print(text)
    if "PRIVMSG" in text and channel in text and "hello" in text:
        irc.send(channel, "Hello!")

