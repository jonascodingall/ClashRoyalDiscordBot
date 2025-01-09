class PlayerClan:
    def __init__(self, badgeId, tag, name, badgeUrls):
        self.badgeId = badgeId
        self.tag = tag
        self.name = name
        self.badgeUrls = badgeUrls

    @classmethod
    def from_json(cls, data):
        return cls(
            badgeId=data.get('badgeId'),
            tag=data.get('tag'),
            name=data.get('name'),
            badgeUrls=data.get('badgeUrls', {})
        )
