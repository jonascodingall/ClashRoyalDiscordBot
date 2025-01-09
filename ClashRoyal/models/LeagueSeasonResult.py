class LeagueSeasonResult:
    def __init__(self, trophies, rank, bestTrophies, id):
        self.trophies = trophies
        self.rank = rank
        self.bestTrophies = bestTrophies
        self.id = id

    @classmethod
    def from_json(cls, data):
        return cls(
            trophies=data.get('trophies'),
            rank=data.get('rank'),
            bestTrophies=data.get('bestTrophies'),
            id=data.get('id')
        )
