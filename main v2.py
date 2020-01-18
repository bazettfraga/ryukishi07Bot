#import irchan
#import disco
import discord
import asyncio
from multiprocessing import Process, Manager, Queue
from multiprocessing.managers import BaseManager
import configparser
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import sys

client = discord.Client()
config = configparser.ConfigParser()
config.read("config.ini")
botToken = config["DISCORD"]["botToken"]

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        print(str(self))

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])
        print(str(e))
        print(str(e.arguments[0]))

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
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

    def get_channel(self):
        for chname, chobj in self.channels.items():
            self.users = sorted(chobj.users())
    
    def disco_command(q_in):
        q_in.get_nowait()
        pass
    
    def do_command(self, e, cmd, q_out):
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
                q_out.put_nowait(users)
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


def ircmain():
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

    bot = TestBot(channel, nickname, server, port)
    bot.start()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

nick = "asdf"

def get_channels():
    return 0

async def cocks():
    print("ochin")
    print(repr(users))

@client.event
async def on_message(message):
    if message.content.startswith("!test"):
        await client.send_message(message.channel, "pong")
        await cocks()




BaseManager.register('SimpleClass', SimpleClass)
manager = BaseManager()
manager.start()
inst = manager.SimpleClass()

p1 = Process(target=client.run, args=(botToken)
p2 = Process(target=ircmain)
p1.start()
p2.start()
p2.join()

#print(inst.get())


while 2:
    pass
