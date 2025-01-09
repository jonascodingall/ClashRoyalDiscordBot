from ClashRoyal.models.RiverRaceParticipant import RiverRaceParticipant


class RiverRaceClan:
    def __init__(self, tag, clanScore, badgeId, name, fame, repairPoints, finishTime, participants: list[RiverRaceParticipant], periodPoints):
        self.tag = tag
        self.clanScore = clanScore
        self.badgeId = badgeId
        self.name = name
        self.fame = fame
        self.repairPoints = repairPoints
        self.finishTime = finishTime
        self.participants = participants  # Liste von RiverRaceParticipant
        self.periodPoints = periodPoints

    @classmethod
    def from_json(cls, data):
        participants = [RiverRaceParticipant.from_json(p) for p in data.get('participants', [])]
        return cls(
            tag=data.get('tag'),
            clanScore=data.get('clanScore'),
            badgeId=data.get('badgeId'),
            name=data.get('name'),
            fame=data.get('fame'),
            repairPoints=data.get('repairPoints'),
            finishTime=data.get('finishTime'),
            participants=participants,
            periodPoints=data.get('periodPoints')
        )