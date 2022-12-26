from dataclasses import dataclass, field
from enum import Enum


class KnightStatus(Enum):
    """Enum class for Knight Status enumerations"""
    ALIVE = "LIVE"
    DROWNED = "DROWNED"
    DIED = "DIED"


@dataclass
class PowerItem:
    """ Class for keeping track of items """

    name: str = None
    location: list[int] = field(default_factory=list)
    status: bool = True
    attack: float = 0
    defence: float = 0
    priority: int = 0

    def disable_item(self):
        self.status = False

    def enable_item(self, location):
        self.status = True
        self.location = location

    def __str__(self):
        """ function will stringify PowerItem object """
        if self.name is None:
            return 'No Description available'
        status = "false" if self.status else "true"
        # return f"{self.name} ({status}) - (attack: {self.attack}, defence: {self.defence}) {self.location}"
        return f"{self.location}, {status}"


@dataclass
class Knight:
    """ Class for keeping track/status of a knight """

    name: str = ''
    location: list[int] = field(default_factory=list)
    status: KnightStatus = KnightStatus.ALIVE
    item_equipped: str = None
    # eligible_items: list[str] = None,
    attack: float = 1
    defence: float = 1
    surprise_attack_bonus: float = 0.5

    def set_to_alive(self):
        self.status = KnightStatus.ALIVE
        self.attack = 1
        self.defence = 1

    def set_to_drowned(self):
        self.status = KnightStatus.DROWNED
        self.attack = 0
        self.defence = 0

    def set_to_death(self):
        self.status = KnightStatus.DIED
        self.attack = 0
        self.defence = 0

    def equip_item(self, item):
        self.attack += item.attack
        self.defence += item.defence
        self.item_equipped = item.name

    def update_position(self, coordinates: list[int]):
        """
            Move Knight only if he is alive otherwise check for drown condition
        """
        if self.status == KnightStatus.ALIVE:
            self.location = coordinates

    def __str__(self):
        """ function will stringify Knight object """
        item: str = "null" if self.item_equipped is None else self.item_equipped
        location = "null" if self.status != KnightStatus.ALIVE else self.location
        return f"{location}, {self.status.value}, {item}, {self.attack}, {self.defence}"

    def to_list(self):
        item: str = "null" if self.item_equipped is None else self.item_equipped
        return [self.location, self.status.value, item, self.attack, self.defence]

