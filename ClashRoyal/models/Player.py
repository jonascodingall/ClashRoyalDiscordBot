from ClashRoyal.models.PlayerAchievementBadge import PlayerAchievementBadge
from ClashRoyal.models.PlayerItemLevel import PlayerItemLevel
from ClashRoyal.models.PlayerLeagueStatistics import PlayerLeagueStatistics


class Player:
    def __init__(self, tag, name, expLevel, trophies, bestTrophies, donations, donationsReceived, currentDeck: list[PlayerItemLevel], supportCards: list[PlayerItemLevel], leagueStatistics: PlayerLeagueStatistics, badges: list[PlayerAchievementBadge]):
        self.tag = tag
        self.name = name
        self.expLevel = expLevel
        self.trophies = trophies
        self.bestTrophies = bestTrophies
        self.donations = donations
        self.donationsReceived = donationsReceived
        self.currentDeck = currentDeck
        self.supportCards = supportCards
        self.leagueStatistics = leagueStatistics
        self.badges = badges

    @classmethod
    def from_json(cls, data):
        currentDeck = [PlayerItemLevel.from_json(item) for item in data.get('currentDeck', [])]
        supportCards = [PlayerItemLevel.from_json(item) for item in data.get('supportCards', [])]
        leagueStatistics = PlayerLeagueStatistics.from_json(data.get('leagueStatistics', {}))
        badges = [PlayerAchievementBadge.from_json(badge) for badge in data.get('badges', [])]

        return cls(
            tag=data.get('tag'),
            name=data.get('name'),
            expLevel=data.get('expLevel'),
            trophies=data.get('trophies'),
            bestTrophies=data.get('bestTrophies'),
            donations=data.get('donations'),
            donationsReceived=data.get('donationsReceived'),
            currentDeck=currentDeck,
            supportCards=supportCards,
            leagueStatistics=leagueStatistics,
            badges=badges
        )
