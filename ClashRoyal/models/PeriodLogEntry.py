from ClashRoyal.models.PeriodLogEntryClan import PeriodLogEntryClan


class PeriodLogEntry:
    def __init__(self, clan: PeriodLogEntryClan, pointsEarned, progressStartOfDay, progressEndOfDay, endOfDayRank, progressEarned, numOfDefensesRemaining, progressEarnedFromDefenses):
        self.clan = clan  # PeriodLogEntryClan
        self.pointsEarned = pointsEarned
        self.progressStartOfDay = progressStartOfDay
        self.progressEndOfDay = progressEndOfDay
        self.endOfDayRank = endOfDayRank
        self.progressEarned = progressEarned
        self.numOfDefensesRemaining = numOfDefensesRemaining
        self.progressEarnedFromDefenses = progressEarnedFromDefenses

    @classmethod
    def from_json(cls, data):
        clan = PeriodLogEntryClan.from_json(data.get('clan', {}))
        return cls(
            clan=clan,
            pointsEarned=data.get('pointsEarned'),
            progressStartOfDay=data.get('progressStartOfDay'),
            progressEndOfDay=data.get('progressEndOfDay'),
            endOfDayRank=data.get('endOfDayRank'),
            progressEarned=data.get('progressEarned'),
            numOfDefensesRemaining=data.get('numOfDefensesRemaining'),
            progressEarnedFromDefenses=data.get('progressEarnedFromDefenses')
        )
