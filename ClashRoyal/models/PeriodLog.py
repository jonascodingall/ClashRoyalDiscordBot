from ClashRoyal.models.PeriodLogEntry import PeriodLogEntry


class PeriodLog:
    def __init__(self, items: list[PeriodLogEntry], periodIndex):
        self.items = items  # Liste von PeriodLogEntry
        self.periodIndex = periodIndex

    @classmethod
    def from_json(cls, data):
        items = [PeriodLogEntry.from_json(item) for item in data.get('items', [])]
        return cls(
            items=items,
            periodIndex=data.get('periodIndex')
        )