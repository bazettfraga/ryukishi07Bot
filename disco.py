import discord
import asyncio
import configparser
#import irchan
import sys
from irchan import irc

client = discord.Client()
config = configparser.ConfigParser()
config.read('config.ini')

botToken = config['DISCORD']['botToken']

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

dicks = 0

async def cocks():
    dicks = 1
    print("ochin")
    irc.send(bytes("NAMES", encoding="UTF8"))

@client.event
async def on_message(message):
    if message.content.startswith("!test"):
        await client.send_message(message.channel, "pong")
        await cocks()
 

#client.run(botToken)
