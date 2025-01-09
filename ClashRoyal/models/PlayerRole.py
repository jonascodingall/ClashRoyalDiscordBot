from enum import Enum


class PlayerRole(Enum):
    NOT_MEMBER = "NOT_MEMBER"
    MEMBER = "MEMBER"
    LEADER = "LEADER"
    ADMIN = "ADMIN"
    COLEADER = "COLEADER"
