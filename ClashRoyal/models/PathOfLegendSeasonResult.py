class PathOfLegendSeasonResult:
    def __init__(self, trophies, rank, leagueNumber):
        self.trophies = trophies
        self.rank = rank
        self.leagueNumber = leagueNumber

    @classmethod
    def from_json(cls, data):
        return cls(
            trophies=data.get('trophies'),
            rank=data.get('rank'),
            leagueNumber=data.get('leagueNumber')
        )
