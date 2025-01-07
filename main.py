import os
import discord
from discord.ext import commands
import cr
import user_service
from dotenv import load_dotenv

# Laden der Umgebungsvariablen
load_dotenv()

# Bot-Initialisierung mit Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
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



if __name__ == "__main__":
    token = os.environ.get('DC_TOKEN')
    if not token:
        print("Discord token not found. Please set the 'DC_TOKEN' environment variable.")
        exit(1)

    bot.run(token)
