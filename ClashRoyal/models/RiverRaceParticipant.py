class RiverRaceParticipant:
    def __init__(self, tag, name, fame, repairPoints, boatAttacks, decksUsed, decksUsedToday):
        self.tag = tag
        self.name = name
        self.fame = fame
        self.repairPoints = repairPoints
        self.boatAttacks = boatAttacks
        self.decksUsed = decksUsed
        self.decksUsedToday = decksUsedToday

    @classmethod
    def from_json(cls, data):
        return cls(
            tag=data.get('tag'),
            name=data.get('name'),
            fame=data.get('fame'),
            repairPoints=data.get('repairPoints'),
            boatAttacks=data.get('boatAttacks'),
            decksUsed=data.get('decksUsed'),
            decksUsedToday=data.get('decksUsedToday')
        )
