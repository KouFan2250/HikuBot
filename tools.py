import discord
import json

help_pages = [
    discord.Embed(title="p1",description="when"),
    discord.Embed(title="p2",description="the"),
    discord.Embed(title="p3",description="imposter"),
    discord.Embed(title="p4",description="is sus")
]
def saveconfig(dik):
    a = open('./config.json','w')
    json.dump(dik,a)
def readconfig():
    a = open('./config.json','r')
    b = json.load(a)
    return b