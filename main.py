import discord
import asyncio
import configparser

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




#@client.event
#async def on_message(message):


client.run(botToken)