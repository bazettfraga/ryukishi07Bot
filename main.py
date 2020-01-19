#import irchan
#import disco
import discord
import asyncio
from multiprocessing import Process, Manager, Queue
import configparser
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import sys
import time

client = discord.Client()
config = configparser.ConfigParser()
config.read("config.ini")
botToken = config["DISCORD"]["botToken"]

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port, qq):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.qq = qq
        #print(str(self))

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_join(self, c, e):
        print("Twatty cakes")
        for chname, chobj in self.channels.items():
            users = sorted(chobj.users())
            self.qq.put(users)

    def on_quit(self, c, e):
        print("Cuntzilla")
        for chname, chobj in self.channels.items():
            users = sorted(chobj.users())
            self.qq.put(users)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])
        print(str(e))
        print(str(e.arguments[0]))

    def on_pubmsg(self, c, e):
        for chname, chobj in self.channels.items():
            users = sorted(chobj.users())
            self.qq.put(users)
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        w
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection
        print(str(self))
        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die() #me_irl
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                #c.notice(nick, "--- Channel statistics ---")
                #c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                print(repr(users))
                opers = sorted(chobj.opers()) #if rena cares
                c.notice(nick, "Opers: " + ", ".join(opers))
                print(repr(opers))
                #voiced = sorted(chobj.voiced())
                #c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp(
                "DCC",
                nick,
                "CHAT chat %s %d"
                % (ip_quad_to_numstr(dcc.localaddress), dcc.localport),
            )
        else:
            c.notice(nick, "Not understood: " + cmd)


def ircmain(qhue):
    import sys

    #if len(sys.argv) != 4:
        #print("Usage: testbot <server[:port]> <channel> <nickname>")
        #sys.exit(1)

    #s = sys.argv[1].split(":", 1)

    server = config["IRC"]["server"]
    try:
        port = int("6667")
    except ValueError:
        print("Error: Erroneous port.")
        sys.exit(1)
    channel = config["IRC"]["channel"]
    nickname = config["IRC"]["nick"]            
    
    bot = TestBot(channel, nickname, server, port, qhue)
    bot.start()

def shootme(botToken,q):
    
    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
    
    blob = q.get()
    print(blob)

    async def getUsers():
        global blob
        if q.empty():
            return blob
        else:
            blob = q.get_nowait()
            return blob

    async def checkUsers(users):
        global blob
        if q.empty():
            print("Works")
            return blob
        else:
            print("FUCK MY ASS")
            holder = q.get_nowait()
            if q.empty():
                print("sense")
            print(blob)
            print(str(holder) + " vs " + str(blob))
            while (blob == holder) and not(q.empty()):
                print("Loopity")
                holder = q.get_nowait()
            blob = holder
            return blob

    @client.event
    async def on_message(message):
        if message.content == "hau!":
            users = await getUsers()
            users = await checkUsers(users)
            #print(users)
            await client.send_message(message.channel, "Users: " + ", ".join(users))
    
    client.run(botToken)

q = Queue() #HURRRRR XD
p1 = Process(target=shootme, args=(botToken,q,))
p2 = Process(target=ircmain, args=(q,))
p1.start()
p2.start()


while 2:
    pass
    #print(q.get())
