class Arena:
    def __init__(self, name, id, iconUrls):
        self.name = name
        self.id = id
        self.iconUrls = iconUrls

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data.get('name'),
            id=data.get('id'),
            iconUrls=data.get('iconUrls', {})
        )
