import irchan
import disco
from multiprocessing import Process, Manager
import configparser

config = configparser.ConfigParser()

config.read("config.ini")

botToken = config["DISCORD"]["botToken"]

p1 = Process(target=disco.client.run, args=(botToken,))
p2 = Process(target=irchan.main)
p1.start()
p2.start()


while 2:
    pass
