import requests
import os

BASE_URL = "https://api.clashroyale.com/v1"
CLAN_ID = "%23YVUQV2YC"


def get_headers():
    """Erstellt die Header für die API-Anfrage."""
    api_key = os.environ.get('CR_KEY')
    if not api_key:
        raise RuntimeError("CR_KEY environment variable not set.")
    return {"Authorization": f"Bearer {api_key}"}


def get_remaining_decks():
    """Holt die verbleibenden Decks aller Clan-Mitglieder."""
    url = f"{BASE_URL}/clans/{CLAN_ID}/currentriverrace"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

    data = response.json()
    participants = data.get("clan", {}).get("participants", [])
    if not participants:
        raise RuntimeError("No participants found in the API response.")

    return [
        f"{player['name']}: remaining decks: {4 - player.get('decksUsedToday', 0)}"
        for player in participants
    ]


def get_player(player_tag: str):
    """Holt die Informationen eines Spielers basierend auf seinem Tag."""
    if not player_tag.startswith("#"):
        raise ValueError("Player tag must start with '#'.")

    url = f"{BASE_URL}/players/{player_tag.replace('#', '%23')}"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

    return response.json()


def get_missing_decks_player():
    """Holt alle Spieler, die ihre Decks noch nicht gespielt haben."""
    url = f"{BASE_URL}/clans/{CLAN_ID}/currentriverrace"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")

    data = response.json()
    participants = data.get("clan", {}).get("participants", [])
    if not participants:
        raise RuntimeError("No participants found in the API response.")

    return [player for player in participants if player.get("decksUsedToday", 0) < 4]
