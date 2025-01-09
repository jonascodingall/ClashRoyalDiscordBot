from ClashRoyal.models.PeriodLog import PeriodLog
from ClashRoyal.models.RiverRaceClan import RiverRaceClan


class CurrentRiverRace:
    def __init__(self, state, clan: RiverRaceClan, clans: list[RiverRaceClan], collectionEndTime, warEndTime, sectionIndex, periodIndex, periodType, periodLogs: list[PeriodLog]):
        self.state = state
        self.clan = clan  # RiverRaceClan
        self.clans = clans  # Liste von RiverRaceClan
        self.collectionEndTime = collectionEndTime
        self.warEndTime = warEndTime
        self.sectionIndex = sectionIndex
        self.periodIndex = periodIndex
        self.periodType = periodType
        self.periodLogs = periodLogs  # Liste von PeriodLog

    @classmethod
    def from_json(cls, data):
        clan = RiverRaceClan.from_json(data.get('clan', {}))
        clans = [RiverRaceClan.from_json(clan_data) for clan_data in data.get('clans', [])]
        periodLogs = [PeriodLog.from_json(log) for log in data.get('periodLogs', [])]

        return cls(
            state=data.get('state'),
            clan=clan,
            clans=clans,
            collectionEndTime=data.get('collectionEndTime'),
            warEndTime=data.get('warEndTime'),
            sectionIndex=data.get('sectionIndex'),
            periodIndex=data.get('periodIndex'),
            periodType=data.get('periodType'),
            periodLogs=periodLogs
        )
