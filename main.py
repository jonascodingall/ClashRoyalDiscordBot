import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from Services import user_service
from ClashRoyal import clashroyal
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# helper functions
async def handle_error(ctx, error_message: str):
    print(f"Error: {error_message}")
    await ctx.send(f"An error occurred: {error_message}")

# events
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    await member.send("""Willkommen auf unserem Discord Server. 
Bitte registriere dich zu allererst im Kanal #Clankrieg mit deinem Spielertag: !register #playertag
Vielen Dank im Voraus!
Wir sind ein Clankriegs-Clan, folglich legen wir großen Wert auf Zuverlässigkeit bezüglich der Clankriegskämpfe.
Falls du einmal nicht kämpfen können solltest, melde dich bitte frühzeitig hier auf dem Discord ab.
Auf viele erfolgreiche Kämpfe und eine gute Gemeinschaft
CR Elite 👑""")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    msg_id = 1327451362606321705
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    role = None
    if payload.message_id == msg_id:
        if str(payload.emoji) == "⚔️":
            role = discord.utils.get(user.guild.roles, name="CLANKRIEG")
        elif str(payload.emoji) == "🪜":
            role = discord.utils.get(user.guild.roles, name="LIGA")
    if role:
        await user.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    msg_id = 1327451362606321705
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    role = None
    if payload.message_id == msg_id:
        if str(payload.emoji) == "⚔️":
            role = discord.utils.get(user.guild.roles, name="CLANKRIEG")
        elif str(payload.emoji) == "🪜":
            role = discord.utils.get(user.guild.roles, name="LIGA")
    if role:
        await user.remove_roles(role)


# commands
@bot.command(name='register')
async def register(ctx: Context, player_tag: str, user: discord.Member = None):
    try:
        dc_target_user = user or ctx.author
        cr_player = clashroyal.get_player(player_tag)

        if not cr_player:
            await ctx.send("Falscher Spieler-Tag")
        else:
            user_service.create({"dc_id": dc_target_user.id, "cr_id": cr_player.tag})
            await ctx.send(f"{dc_target_user.mention} registriert als {cr_player.name}")

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="unregister")
async def unregister(ctx: Context, user: discord.Member = None):
    try:
        dc_target_user = user or ctx.author
        user_service.delete(dc_target_user.id)

        await ctx.send(f"{dc_target_user.id} unregistriert")

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="remind")
def remind(ctx: Context, options: str):
    pass

if __name__ == "__main__":
    token = os.environ.get('DC_TOKEN')
    if not token:
        print("Discord token not found. Please set the 'DC_TOKEN' environment variable.")
        exit(1)

    bot.run(token)
