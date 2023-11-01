import discord 
from discord.ext import commands
from dic import *
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("SpeedBot est en ligne.")

@bot.command()
async def aide(ctx : commands.Context):
    await ctx.send("Je suis la pour t'aider !")

@bot.command()
async def eteindre(ctx: commands.Context):
    await ctx.send("SpeedBot s'éteint.")
    await bot.close()

@bot.event
async def on_message(message : discord.Message):
    if message.author.bot == True:
        return

    if message.content in bjr:
        reponse = random.choice(reponse_bjr)
        await message.channel.send(reponse)

if __name__ == '__main__':
    bot.run("MTE2OTM3NTA1NjE0MTUwNDY1Mw.Gnl9yt.6OFwtPUhNwDB-tabRe6kKl1HKobJWKHdxjTj7Y")