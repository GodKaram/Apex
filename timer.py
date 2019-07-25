import discord
from discord.ext import commands, tasks
from discord.ext.tasks import loop
import numpy as np
import datetime
import asyncio
import pickle

client = discord.Client()
CHL= 603191134025547787


@client.event
async def on_ready():
    print("ready")
    channel = client.get_channel(CHL)
    await channel.send("Bot is Ready")


@loop(seconds=60)
async def my_background_task():
    await client.wait_until_ready()
    checktimenow()
    file = open('chboss', "rb")
    fload = pickle.load(file)
    fcheck = fload
    file.close()
    timecheck = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    for key in fcheck:
        bosslist = fcheck[key]
        if timecheck == bosslist[0] - datetime.timedelta(minutes=5):
            if bosslist[3] <= 2:
                channel = client.get_channel(598927749784272898)
                await channel.send("**{}** : **5 min** Till Due | Reset Counter: {}".format(key, bosslist[3]))
        if timecheck == bosslist[0] - datetime.timedelta(minutes=10):
            if bosslist[3] <= 2:
                channel = client.get_channel(598927749784272898)
                await channel.send("**{}** : **10 min** Till Due | Reset Counter: {}".format(key, bosslist[3]))
        if timecheck == bosslist[0]:
            if bosslist[3] <= 2:
                channel = client.get_channel(CHL)
                await channel.send("**{}** : is Due | Reset Counter: {}".format(key, bosslist[3]))
                if bosslist[2] == 0:
                    bosslist[0] = bosslist[0] + datetime.timedelta(minutes=bosslist[1])
                    bosslist[3] = bosslist[3] + 1
                    fcheck[key] = bosslist
                    file = open('chboss', "wb")
                    pickle.dump(fcheck, file)
                    file.close()
                    file = open('chboss', "rb")
                    fload = pickle.load(file)
                    fcheck = fload
                    file.close()
                    channel = client.get_channel(CHL)
                    await channel.send("**{}** : time reseted ".format(key))





@client.event
async def on_message(message):
    if message.content.startswith('.bosstime'):
        file = open('chboss', "rb")
        fload = pickle.load(file)
        file.close()
        timenowutc = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        for key in fload:
            btime = fload[key]
            bftime = btime[0] - timenowutc
            if timenowutc > btime[0]:
                channel = client.get_channel(CHL)
                await channel.send("**{}** is Due !!!!!".format(key))
            else:
                channel = client.get_channel(CHL)
                await channel.send("**{}** time : **{}** | Auto Counter: {}".format(key, bftime, btime[3]))
        file = open('chboss', "rb")
        fload = pickle.load(file)
        fcheck = fload
        file.close()

    if message.content.startswith('.checktime'):
        checktimenow()
        channel = client.get_channel(CHL)
        await channel.send("Time is Checked")
    if message.content.startswith('.helpch'):
        channel = client.get_channel(CHL)
        await channel.send("-   **.reset.boss** - reset the time of (boss=specified boss)")
        await channel.send("-   **.set.boss.Tm** - set the time (boss=specified boss) with T time")
        await channel.send("-   **.bosstime**  - shows all boss time ")
        await channel.send("-   **.checktime** - In case of any error use it.")
        await channel.send("## Bot will automatically reset time with a counter if not reseted manually ## ")

    file = open('chboss', "rb")
    fload = pickle.load(file)
    file.close()
    for key in fload:
        bosslist = fload[key]
        if message.content.startswith('.reset.{}'.format(key)):
            bosslist[0] = datetime.datetime.utcnow().replace(second=0, microsecond=0) + datetime.timedelta(
                minutes=bosslist[1])
            bosslist[3] = 0
            fload[key] = bosslist
            file = open("chboss", "wb")
            pickle.dump(fload, file)
            file.close()
            file = open("chboss", "rb")
            fload = pickle.load(file)
            fcheck = fload
            file.close()
            channel = client.get_channel(CHL)
            await channel.send("**{}** is Reseted".format(key))
        for n in range(0, 3000):
            if message.content.startswith('.set.{}.{}m'.format(key, n)):
                bosslist[0] = datetime.datetime.utcnow().replace(second=0, microsecond=0) + datetime.timedelta(minutes=n)
                bosslist[3] = 0
                fload[key] = bosslist
                file = open("chboss", "wb")
                pickle.dump(fload, file)
                file.close()
                file = open("chboss", "rb")
                fload = pickle.load(file)
                fcheck = fload
                file.close()
                channel = client.get_channel(CHL)
                await channel.send("**{}** is now set ".format(key))

            if message.content.startswith('.set.{}.spawntime.{}m'.format(key, n)):
                bosslist[1] = n
                fload[key] = bosslist
                file = open("chboss", "wb")
                pickle.dump(fload, file)
                file.close()
                file = open("chboss", "rb")
                fload = pickle.load(file)
                fcheck = fload
                file.close()
                channel = client.get_channel(CHL)
                await channel.send("**{}** spawn time is {} min ".format(key, bosslist[1]))



def checktimenow():
    file = open('chboss', "rb")
    fload = pickle.load(file)
    fcheck = fload
    file.close()
    timecheck = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    for key in fcheck:
        bosslist = fcheck[key]
        if timecheck > bosslist[0]:
            if bosslist[2] == 0:
                while timecheck > bosslist[0]:
                    bosslist[0] = bosslist[0] + datetime.timedelta(minutes=bosslist[1])
                    bosslist[3] = bosslist[3] + 1
                fcheck[key] = bosslist
                file = open('chboss', "wb")
                pickle.dump(fcheck, file)
                file.close()
    return

my_background_task.start()

client.run('NTk5MTgxNDYwODQ2NDExNzgz.XSiuHw.LP7Y3QaRmkxMFXVrvCrHPXxuOmA')
