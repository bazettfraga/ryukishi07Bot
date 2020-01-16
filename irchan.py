import socket
import sys
import ssl
import time
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

channel = config['IRC']['channel']
server = config['IRC']['server']
botnick = config['IRC']['nick']
port = 6666
password = ""

### Tail
tail_files = [
            '/tmp/file-to-tail.txt'
            ]

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
#irc = ssl.wrap_socket(irc_C)
def main():
    print("Establishing connection to [%s]" % (server))
    # Connect
    irc.connect((server, port))
    irc.setblocking(False)
    irc.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :meLon-Test\n", encoding="UTF8"))
    irc.send(bytes("NICK "+ botnick +"\n", encoding="UTF8"))
    tail_line = []
    for i, tail in enumerate(tail_files):
            tail_line.append('')


    while True:
        time.sleep(2)

                        # Tail Files
        for i, tail in enumerate(tail_files):
            #try:
                #f = open(tail, 'r')
                #line = f.readlines()[-1]
                #f.close()
                #if tail_line[i] != line:
                    #tail_line[i] = line
                    #irc.send(bytes("PRIVMSG %s :%s" % (channel, line) ,encoding="UTF8"))
            #except Exception as e:
                #print ("Error with file %s" % (tail))
                #print (e)
            try:
                text=str(irc.recv(2040))
                print (text)
                if text.find('PING') != -1:
                    irc.send(bytes('PONG ' + text.split() [1] + '\r\n' ,encoding="UTF8"))
                    irc.send(bytes("PRIVMSG nickserv :identify %s %s\r\n" % (botnick, password), encoding="UTF8"))
                    irc.send(bytes("JOIN "+ channel +"\n", encoding="UTF8"))
                    #irc.send(bytes("NAMES", encoding="UTF8"))
            except Exception:
                continue       
