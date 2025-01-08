import os
import discord
from discord.ext import commands
import cr
import user_service
from dotenv import load_dotenv

# Laden der Umgebungsvariablen
load_dotenv()

# Bot-Initialisierung mit Intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


# Hilfsfunktion: Fehlerbehandlung
async def handle_error(ctx, error_message: str):
    print(f"Error: {error_message}")
    await ctx.send(f"An error occurred: {error_message}")


@bot.event
async def on_ready():
    """Wird ausgelöst, wenn der Bot erfolgreich gestartet wurde."""
    print(f"Bot logged in as {bot.user}")


@bot.command()
async def remaining(ctx, lang: str = 'en'):
    """Zeigt die verbleibenden Decks aller Clan-Mitglieder an."""
    try:
        result_list = cr.get_remaining_decks()
        if not result_list:
            await ctx.send("No data available.")
            return

        max_chars_per_message = 2000
        message = ""

        for item in result_list:
            if len(message) + len(item) + 1 > max_chars_per_message:
                await ctx.send(message)
                message = ""
            message += f"{item}\n"

        if message:
            await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))


@bot.command()
async def register(ctx, player_tag: str, lang: str = 'en'):
    """Registriert einen Discord-Nutzer mit einem Clash Royale-Spieler-Tag."""
    try:
        user_id = ctx.author.id
        cr_user = cr.get_player(player_tag)

        if not cr_user or "tag" not in cr_user or "name" not in cr_user:
            await ctx.send("Invalid player tag or player not found.")
            return

        user_service.create({"dc_id": user_id, "cr_id": cr_user["tag"]})
        await ctx.send(f"{ctx.author.mention} registered as {cr_user['name']}")

    except Exception as e:
        await handle_error(ctx, str(e))


@bot.command()
async def unregister(ctx, lang: str = 'en'):
    """Entfernt die Registrierung eines Discord-Nutzers."""
    try:
        user_service.delete(ctx.author.id)
        await ctx.send(f"{ctx.author.mention} unregistered")
    except Exception as e:
        await handle_error(ctx, str(e))


@bot.command()
async def remind(ctx, lang: str = 'en'):
    """Erinnert Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        missing_players = cr.get_missing_decks_player()
        if not missing_players:
            await ctx.send("All players have completed their CV.")
            return

        max_chars_per_message = 2000
        message = ""

        for player in missing_players:
            user_link = user_service.read_cr(player.get("tag"))
            if user_link and "dc_id" in user_link:
                user = await bot.fetch_user(user_link["dc_id"])
                if user:
                    message += f"{user.mention}, please do your CV!\n"
            else:
                message += f"{player.get('name')}, please do your CV!\n"

            # Nachricht senden, wenn die maximale Zeichenanzahl erreicht ist
            if len(message) > max_chars_per_message:
                await ctx.send(message)
                message = ""

        # Verbleibende Nachricht senden
        if message:
            await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="remind-private")
async def remind_private(ctx, lang: str = 'en'):
    """Schickt private Erinnerungen an Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        missing_players = cr.get_missing_decks_player()
        if not missing_players:
            await ctx.send("All players have completed their CV.")
            return


        for player in missing_players:
            user_link = user_service.read_cr(player.get("tag"))
            if user_link and "dc_id" in user_link:
                user = await bot.fetch_user(user_link["dc_id"])
                if user:
                    await user.send("Please complete your CV!")


    except Exception as e:
        await handle_error(ctx, str(e))

@bot.command(name="list-registered-cr")
async def list_registered_cr(ctx, lang: str = 'en'):
    """Schickt private Erinnerungen an Nutzer, die ihre Decks noch nicht gespielt haben."""
    try:
        user_list = user_service.load_data()
        cr_members = cr.get_clan_members()

        max_chars_per_message = 2000
        message = ""

        for member in cr_members:
            if member["tag"] not in [user["cr_id"] for user in user_list]:
                message += f"{member["name"]} has´nt registered jet\n"
        await ctx.send(message)

    except Exception as e:
        await handle_error(ctx, str(e))


@bot.command(name="list-registered-dc")
async def list_registered_dc(ctx, lang: str = 'en'):
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
        cr_members = cr.get_clan_members()  # Lade die Clan-Mitglieder

        for cr_member in cr_members:
            # Überprüfe, ob das Clan-Mitglied auch in der user_list vorhanden ist
            user_data = next((user for user in user_list if user["cr_id"] == cr_member["tag"]), None)
            if user_data:
                # Hole die Discord-ID (dc_id) des Benutzers aus der user_list
                dc_id = user_data["dc_id"]
                cr_member_role = cr_member["role"]  # Hole die Rolle des Clan-Mitglieds

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
