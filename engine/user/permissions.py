from enum import Enum


class Permissions:
    def __init__(self, title: str, perms_list: list[str]):
        self._title = title
        self._perms_list = perms_list

    @property
    def title(self) -> str:
        return self._title

    def check_perm(self, perm: str):
        if perm.lower() in self._perms_list:
            return True
        return False

    def __eq__(self, other):
        return self.title.lower() == other.title.lower()

    def __ne__(self, other):
        return self.title.lower() != other.title.lower()


class PermissionsGroups(Enum):
    UNKNOWN = Permissions("Гость", [])
    CLIENT = Permissions("Клиент", [])
    STAFF = Permissions("Работник", ["invite.create"])

    @classmethod
    def get_from_technical_name(cls, technical: str):

        for group in cls:
            if group.name == technical:
                return group
        raise ValueError("Unknown permisssipns group!")


