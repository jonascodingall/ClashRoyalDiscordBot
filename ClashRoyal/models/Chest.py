class Chest:
    def __init__(self, index, name):
        self.index = index
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(
            index=data.get("index"),
            name=data.get("name")
        )