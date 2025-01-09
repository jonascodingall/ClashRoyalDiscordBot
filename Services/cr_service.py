from ClashRoyal import cr_api

CV_CLAN_TAG = "#YVUQV2YC"

# helper
def format_tag(tag):
    return tag.replace("#", "%23")

# main functions
def get_clan_members():
    return cr_api.get_clan_members(format_tag(CV_CLAN_TAG))

def get_currentriverrace():
    return cr_api.get_clan_currentriverrace(format_tag(CV_CLAN_TAG))

def get_player(player_tag):
    return cr_api.get_player(format_tag(player_tag))


# special functions
def missing_decks_currentriverrace():
    currentriverrace = get_currentriverrace()

    missing = []
    for participant in currentriverrace.clan.participants:
        if participant.decksUsed < 4:
            missing.append(participant)

    return missing