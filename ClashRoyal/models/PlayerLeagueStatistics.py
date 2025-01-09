from ClashRoyal.models.LeagueSeasonResult import LeagueSeasonResult


class PlayerLeagueStatistics:
    def __init__(self, bestSeason: LeagueSeasonResult, currentSeason: LeagueSeasonResult, previousSeason: LeagueSeasonResult):
        self.bestSeason = bestSeason
        self.currentSeason = currentSeason
        self.previousSeason = previousSeason

    @classmethod
    def from_json(cls, data):
        bestSeason = LeagueSeasonResult.from_json(data.get('bestSeason', {}))
        currentSeason = LeagueSeasonResult.from_json(data.get('currentSeason', {}))
        previousSeason = LeagueSeasonResult.from_json(data.get('previousSeason', {}))

        return cls(
            bestSeason=bestSeason,
            currentSeason=currentSeason,
            previousSeason=previousSeason
        )
