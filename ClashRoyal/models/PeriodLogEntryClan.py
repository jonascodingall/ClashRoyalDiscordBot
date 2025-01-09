class PeriodLogEntryClan:
    def __init__(self, tag):
        self.tag = tag

    @classmethod
    def from_json(cls, data):
        return cls(
            tag=data.get('tag')
        )