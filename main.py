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
        for chname, chobj in self.channels.items():
            users = sorted(chobj.users())
            self.qq.put(users)
    
    def on_quit(self, c, e):
        for chname, chobj in self.channels.items():
            users = sorted(chobj.users())
            self.qq.put(users)

    def on_pubmsg(self, c, e):
        for chname, chobj in self.channels.items():
            users = sorted(chobj.users())
            self.qq.put(users)


def ircmain(qhue):
    import sys

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
            return blob
        else:
            holder = q.get_nowait()
            while (blob == holder) and not(q.empty()):
                holder = q.get_nowait()
            blob = holder
            return blob

    @client.event
    async def on_message(message):
        if message.content.lower() == "hau!":
            users = await getUsers()
            users = await checkUsers(users)
            await message.channel.send("These Wonderlanders are currently online: " + ", ".join(users))
    
    while True:
            try:
                client.loop.run_until_complete(client.start(botToken))
            except BaseException:
                time.sleep(5)

    client.run(botToken)

q = Queue() #HURRRRR XD
p1 = Process(target=shootme, args=(botToken,q,))
p2 = Process(target=ircmain, args=(q,))
p1.start()
p2.start()
