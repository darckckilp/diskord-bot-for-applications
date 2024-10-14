import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("bot is rady!")


bot.load_extensions('cogs')


bot.run("your bot token")