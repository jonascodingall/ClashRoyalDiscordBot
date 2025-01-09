class PlayerItemLevel:
    def __init__(self, id, rarity, count, level, starLevel, evolutionLevel, used, name, maxLevel, elixirCost, maxEvolutionLevel, iconUrls):
        self.id = id
        self.rarity = rarity
        self.count = count
        self.level = level
        self.starLevel = starLevel
        self.evolutionLevel = evolutionLevel
        self.used = used
        self.name = name
        self.maxLevel = maxLevel
        self.elixirCost = elixirCost
        self.maxEvolutionLevel = maxEvolutionLevel
        self.iconUrls = iconUrls

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data.get('id'),
            rarity=data.get('rarity'),
            count=data.get('count'),
            level=data.get('level'),
            starLevel=data.get('starLevel'),
            evolutionLevel=data.get('evolutionLevel'),
            used=data.get('used'),
            name=data.get('name'),
            maxLevel=data.get('maxLevel'),
            elixirCost=data.get('elixirCost'),
            maxEvolutionLevel=data.get('maxEvolutionLevel'),
            iconUrls=data.get('iconUrls', {})
        )
