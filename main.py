import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from Services import user_service
from Services import cr_service
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# Hilfsfunktion: Fehlerbehandlung
async def handle_error(ctx, error_message: str):
    print(f"Error: {error_message}")
    await ctx.send(f"An error occurred: {error_message}")

# events
@bot.event
async def on_ready():
    """Wird ausgelöst, wenn der Bot erfolgreich gestartet wurde."""
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

# commands
@bot.command(name='register')
async def register(ctx: Context, player_tag: str, user: discord.Member = None, lang: str = 'en'):
    try:
        dc_target_user = user or ctx.author

        cr_user = cr_service.get_player(player_tag)

        if not cr_user:
            await ctx.send("Invalid player tag or player not found.")
        else:
            user_service.create({"dc_id": dc_target_user.id, "cr_id": cr_user.tag})
            await ctx.send(f"{dc_target_user.mention} registered as {cr_user.name}")

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="unregister")
async def unregister(ctx: Context, user: discord.Member = None , lang: str = 'en'):
    try:
        dc_target_user = user or ctx.author
        user_service.delete(dc_target_user.id)
        await ctx.send(f"{dc_target_user.id} unregistered")

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command("remind-cv")
async def remind_cv(ctx, lang: str = 'en'):
    """Erinnert Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        missing_decks = cr_service.missing_decks_currentriverrace()
        if not missing_decks:
            await ctx.send("All players have completed their CV.")
            return

        max_chars_per_message = 2000
        message = ""

        for participant in missing_decks:
            user_link = user_service.read_cr(participant.tag)
            if user_link and "dc_id" in user_link:
                user = await bot.fetch_user(user_link["dc_id"])
                if user:
                    message += f"{user.mention}, please do your CV!\n"

        # Verbleibende Nachricht senden
        if message:
            await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command("remind-cv-all")
async def remind_cv_all(ctx, lang: str = 'en'):
    """Erinnert Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        missing_decks = cr_service.missing_decks_currentriverrace()
        if not missing_decks:
            await ctx.send("All players have completed their CV.")
            return

        max_chars_per_message = 2000
        message = ""

        for participant in missing_decks:
            user_link = user_service.read_cr(participant.tag)
            if user_link and "dc_id" in user_link:
                user = await bot.fetch_user(user_link["dc_id"])
                if user:
                    message += f"{user.mention}, please do your CV!\n"
            else:
                message += f"{participant.name}, please do your CV!\n"

        # Verbleibende Nachricht senden
        if message:
            await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="remind-cv-private")
async def remind_cv_private(ctx, lang: str = 'en'):
    """Schickt private Erinnerungen an Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        missing_decks = cr_service.missing_decks_currentriverrace()
        if not missing_decks:
            await ctx.send("All players have completed their CV.")
            return


        for participant in missing_decks:
            user_link = user_service.read_cr(participant.tag)
            if user_link and "dc_id" in user_link:
                user = await bot.fetch_user(user_link["dc_id"])
                if user:
                    await user.send("Please complete your CV!")

        await ctx.send("Sended a private reminder!")


    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="list-unregistered-cr")
async def list_unregistered_cr(ctx, lang: str = 'en'):
    """Schickt private Erinnerungen an Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        user_list = user_service.load_data()
        cr_members = cr_service.get_clan_members()

        message = ""

        for member in cr_members.members:
            if member.tag not in [user["cr_id"] for user in user_list]:
                message += f"{member.name} has´nt registered jet\n"
        await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="list-unregistered-dc")
async def list_unregistered_dc(ctx, lang: str = 'en'):
    """Schickt private Erinnerungen an Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        user_list = user_service.load_data()
        dc_members = ctx.guild.members

        max_chars_per_message = 2000
        message = ""
        for member in dc_members:
            if not member.bot:
                if member.id not in [user["dc_id"] for user in user_list]:
                    message += f"{member.mention} has´nt registered jet\n"

        await ctx.send(message)


    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="remind-unregistered-private")
async def remind_unregistered_private(ctx, lang: str = 'en'):
    """Schickt private Erinnerungen an Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        user_list = user_service.load_data()
        dc_members = ctx.guild.members

        for member in dc_members:
            if not member.bot:
                if member.id not in [user["dc_id"] for user in user_list]:
                    await member.send(f"Please register yourself ")


    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="update-roles")
async def update_roles(ctx, lang: str = 'en'):
    try:
        user_list = user_service.load_data()  # Lade die Benutzerliste
        cr_members = cr_service.get_clan_members()  # Lade die Clan-Mitglieder

        for cr_member in cr_members.members:
            # Überprüfe, ob das Clan-Mitglied auch in der user_list vorhanden ist
            user_data = next((user for user in user_list if user["cr_id"] == cr_member.tag), None)
            if user_data:
                # Hole die Discord-ID (dc_id) des Benutzers aus der user_list
                dc_id = user_data["dc_id"]
                cr_member_role = cr_member.role  # Hole die Rolle des Clan-Mitglieds

                # Hole das Member-Objekt aus dem Server anhand der Discord-ID
                member = ctx.guild.get_member(dc_id)
                if member:
                    # Bestimme den Rollennamen basierend auf der Rolle des Clan-Mitglieds
                    role_name = ""
                    if cr_member_role == "elder":
                        role_name = "Ältester"
                    elif cr_member_role == "admin":
                        role_name = "Vize"
                    elif cr_member_role == "coleader":
                        role_name = "Vize-Anführer"
                    elif cr_member_role == "leader":
                        role_name = "Anführer"

                    # Hole die Rolle aus dem Server
                    role = discord.utils.get(ctx.guild.roles, name=role_name)

                    if role:
                        # Füge die Rolle hinzu, wenn sie noch nicht zugewiesen ist
                        if role not in member.roles:
                            await member.add_roles(role)
                            await ctx.send(f"Rolle '{role_name}' wurde {member.name} zugewiesen.")
    except Exception as e:
        await ctx.send(f"Es gab einen Fehler: {e}")

@bot.command(name="upcomingchests")
async def upcomingchests(ctx: Context, user: discord.Member = None, count = None, lang: str = 'en'):
    try:
        dc_target_user = user or ctx.author
        cr_member = user_service.read_dc(dc_target_user.id)
        upcoming_chests = cr_service.get_upcomingchests(cr_member["cr_id"])
        message = f"This are your upcoming chests {dc_target_user.mention}:\n\n"
        if count:
            for i in range(count):
                chest = upcoming_chests.chests[i]
                message += f"{chest.name} in {chest.index} Wins\n"
        else:
            for chest in upcoming_chests.chests:
                message += f"{chest.name} in {chest.index + 1} Wins\n"

        await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))

if __name__ == "__main__":
    token = os.environ.get('DC_TOKEN')
    if not token:
        print("Discord token not found. Please set the 'DC_TOKEN' environment variable.")
        exit(1)

    bot.run(token)
