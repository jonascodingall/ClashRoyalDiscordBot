class PlayerAchievementBadge:
    def __init__(self, iconUrls, maxLevel, progress, level, target, name):
        self.iconUrls = iconUrls
        self.maxLevel = maxLevel
        self.progress = progress
        self.level = level
        self.target = target
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(
            iconUrls=data.get('iconUrls', {}),
            maxLevel=data.get('maxLevel'),
            progress=data.get('progress'),
            level=data.get('level'),
            target=data.get('target'),
            name=data.get('name')
        )
