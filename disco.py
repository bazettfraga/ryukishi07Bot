import discord
import asyncio
import configparser
#import irchan
import sys
from irchan import *

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

def get_channels():
    return 0

async def cocks():
    print("ochin")
    TestBot.disco_command("e")

@client.event
async def on_message(message):
    if message.content.startswith("!test"):
        await client.send_message(message.channel, "pong")
        await cocks()
 

#client.run(botToken)
