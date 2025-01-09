from ClashRoyal.models.Arena import Arena


class ClanMember:
    def __init__(self, clanChestPoints, lastSeen, arena: Arena, tag, name, role, expLevel, trophies, clanRank, previousClanRank, donations, donationsReceived):
        self.clanChestPoints = clanChestPoints
        self.lastSeen = lastSeen
        self.arena = arena  # Arena
        self.tag = tag
        self.name = name
        self.role = role
        self.expLevel = expLevel
        self.trophies = trophies
        self.clanRank = clanRank
        self.previousClanRank = previousClanRank
        self.donations = donations
        self.donationsReceived = donationsReceived

    @classmethod
    def from_json(cls, data):
        arena = Arena.from_json(data.get('arena', {}))
        return cls(
            clanChestPoints=data.get('clanChestPoints'),
            lastSeen=data.get('lastSeen'),
            arena=arena,
            tag=data.get('tag'),
            name=data.get('name'),
            role=data.get('role'),
            expLevel=data.get('expLevel'),
            trophies=data.get('trophies'),
            clanRank=data.get('clanRank'),
            previousClanRank=data.get('previousClanRank'),
            donations=data.get('donations'),
            donationsReceived=data.get('donationsReceived')
        )