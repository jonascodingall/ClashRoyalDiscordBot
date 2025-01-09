class PlayerAchievementProgress:
    def __init__(self, stars, value, name, target, info, completionInfo):
        self.stars = stars
        self.value = value
        self.name = name
        self.target = target
        self.info = info
        self.completionInfo = completionInfo

    @classmethod
    def from_json(cls, data):
        return cls(
            stars=data.get('stars'),
            value=data.get('value'),
            name=data.get('name'),
            target=data.get('target'),
            info=data.get('info'),
            completionInfo=data.get('completionInfo')
        )
