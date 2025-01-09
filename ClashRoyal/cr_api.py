import requests
import os

from ClashRoyal.models.ClanMemberList import ClanMemberList
from ClashRoyal.models.CurrentRiverRace import CurrentRiverRace
from ClashRoyal.models.Player import Player

BASE_URL = "https://api.clashroyale.com/v1"


# Helper
def get_headers():
    api_key = os.environ.get('CR_KEY')
    if not api_key:
        raise RuntimeError("CR_KEY environment variable not set.")
    return {"Authorization": f"Bearer {api_key}"}

def handle_request_exception(e):
    """Hilfsfunktion zur Fehlerbehandlung bei API-Anfragen."""
    print(f"An error occurred: {e}")
    raise Exception(f"API request failed: {e}")

def make_request(url):
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        handle_request_exception(e)


# Main API Funktionen
def get_clan_members(clan_tag):
    url = f"{BASE_URL}/clans/{clan_tag}/members"
    members_data = make_request(url)
    return ClanMemberList.from_json(members_data)

def get_clan_currentriverrace(clan_tag):
    url = f"{BASE_URL}/clans/{clan_tag}/currentriverrace"
    current_race_data = make_request(url)
    return CurrentRiverRace.from_json(current_race_data)

def get_player(player_tag):
    url = f"{BASE_URL}/players/{player_tag}"
    player_data = make_request(url)
    return Player.from_json(player_data)