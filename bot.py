import discord
from discord.ext import commands
from discord.ui import Button, View
import os

# Discord-Bot-Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Verfügbare Streams
STREAMS = {
    "lofi": "https://streams.ilovemusic.de/iloveradio17.mp3",  # Lofi Hip Hop
    "Hardstyle": "https://streams.ilovemusic.de/iloveradio21.mp3",
    "pop": "https://streams.ilovemusic.de/iloveradio1.mp3",   # Mainstream Pop
    "sunlive": "http://stream.sunshine-live.de/live/mp3-192",  # Sunshine Live
    "dnb": "https://dnbradio.nl/dnbradio_main.mp3"  # Drum and Bass
}

# Überprüfe, ob die Umgebungsvariable gesetzt ist
token = os.getenv("Discord_Bot_Key")
if not token:
    print("ERROR: Discord_Bot_Key ist nicht gesetzt!")
    exit(1)  # Stoppe den Bot, falls der Token nicht gesetzt ist
else:
    print("Discord_Bot_Key ist korrekt gesetzt.")

# Bot tritt dem Sprachkanal bei und sendet Buttons
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            await channel.connect()
            await ctx.send(f"Ich bin dem Sprachkanal {channel} beigetreten!")

            # Erstelle Buttons für die verfügbaren Streams
            view = View()
            for name, url in STREAMS.items():
                button = Button(label=name.capitalize(), style=discord.ButtonStyle.primary)

                async def play_stream(interaction, url=url, stream_name=name):
                    if ctx.voice_client:
                        ctx.voice_client.stop()  # Stoppe aktuelle Wiedergabe
                        ctx.voice_client.play(discord.FFmpegPCMAudio(url))
                        await interaction.response.send_message(f"Ich spiele jetzt den Stream: {stream_name}")

                button.callback = play_stream
                view.add_item(button)

            await ctx.send("Wähle einen Stream aus:", view=view)
        else:
            await ctx.send("Ich bin bereits in einem Sprachkanal!")
    else:
        await ctx.send("Du musst dich in einem Sprachkanal befinden, damit ich beitreten kann.")

# Bot verlässt den Sprachkanal
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Ich habe den Sprachkanal verlassen.")
    else:
        await ctx.send("Ich bin in keinem Sprachkanal!")

# Run the bot
bot.run(token)
