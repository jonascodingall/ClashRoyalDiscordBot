import os
import discord
from discord.ext import commands
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

# commands
@bot.command(name='register')
async def register(ctx, player_tag: str, lang: str = 'en'):
    try:
        user_id = ctx.author.id
        cr_user = cr_service.get_player(player_tag)

        if not cr_user:
            await ctx.send("Invalid player tag or player not found.")
            return

        user_service.create({"dc_id": user_id, "cr_id": cr_user.tag})
        await ctx.send(f"{ctx.author.mention} registered as {cr_user.name}")

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="unregister")
async def unregister(ctx, lang: str = 'en'):
    try:
        user_service.delete(ctx.author.id)
        await ctx.send(f"{ctx.author.mention} unregistered")
    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="remaining-decks")
async def remaining_decks(ctx, lang: str = 'en'):
    try:
        result_list = cr_service.get_currentriverrace()

        if not result_list:
            await ctx.send("No data available.")
            raise Exception()

        message = ""

        for participants in result_list.clan.participants:
            message += f"**{participants.name}** : {4 - participants.decksUsedToday}\n"

        await ctx.send(message)

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

if __name__ == "__main__":
    token = os.environ.get('DC_TOKEN')
    if not token:
        print("Discord token not found. Please set the 'DC_TOKEN' environment variable.")
        exit(1)

    bot.run(token)
