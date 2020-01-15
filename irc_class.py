import socket
import sys


class IRC:

    irc = socket.socket()
  
    def __init__(self):  
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, chan, msg):
        self.irc.send(bytes("PRIVMSG " + chan + " " + msg + "n"))

    def connect(self, server, channel, botnick):
        #defines the socket
        print("connecting to: "+server)
        self.irc.connect((server, 6666))                                                         #connects to the server
        self.irc.send(bytes("USER " + botnick + " " + botnick +" " + botnick + " :This is a fun bot!n", encoding="utf8")) #user authentication
        self.irc.send(bytes("NICK " + botnick + "n", encoding="utf8"))
        self.irc.send(bytes("JOIN " + channel + "n", encoding="utf8"))

    def get_text(self):
        text=self.irc.recv(2048).decode("UTF-8")  #receive the text

        if text.find('PING') != -1:                      
            self.irc.send(bytes('PONG ' + text.split() [1] + 'rn'), encoding="utf8") 

        return text
