import discord
from discord.ext import  commands
import youtube_dl
import os

Tokenul = '****'

client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url :str):

    cantecul_aici = os.path.isfile("song.mp3")
    try:
        if cantecul_aici:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait")
        return
    #voiceCanal = discord.utils.get(ctx.guild.voice_channels, name = 'Camera duelurilor')
    voiceCanal = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    await voiceCanal.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessor':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".webm"):
            os.rename(file,"song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async  def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send('Not connected!')

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('No song')

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("idk")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run(Tokenul)