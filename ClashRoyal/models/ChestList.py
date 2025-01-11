from ClashRoyal.models.Chest import Chest


class ChestList:
    def __init__(self, chests: list[Chest]):
        self.chests = chests

    @classmethod
    def from_json(cls, data):
        return cls(
            chests=[Chest.from_json(chest_data) for chest_data in data.get('items', [])]
            )
