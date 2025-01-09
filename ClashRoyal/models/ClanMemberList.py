from ClashRoyal.models.ClanMember import ClanMember


class ClanMemberList:
    def __init__(self, members: list[ClanMember]):
        self.members = members  # Liste von ClanMember-Objekten

    @classmethod
    def from_json(cls, data):
        members = [ClanMember.from_json(member_data) for member_data in data.get("items")]
        return cls(members)