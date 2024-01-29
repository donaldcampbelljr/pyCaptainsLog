# from collections.abc import MutableMapping
# from typing import Any

class Ship():
    """
    The main class that the ship, aka the PLAYER.
    """

    def __init__(self, name, location) -> None:
        """

        :param name:
        :param location: a StarSystem of Class StarSystem
        """

        self.name = name
        self.location = location
        self.health = 40
        self.crew = 50

        self.strength = 6
        self.science = 8
        self.diplomacy = 10

        self.level = 1
        self.experience = 0
        self.exp_next_level = self.level * 100 * 1.20
        self.cargo = {}

        self.cargo.update({"Tribbles":"They don't do much, other than make more tribbles."})

    # def __getitem__(self, __key: Any) -> Any:
    #     return super().__getitem__(__key)

    def scan(self) -> None:
        """
        "Scan" the system, read the system info to the player.
        """
        print(f"Attacking with strength: {self.science}")

    def attack(self) -> None:
        """
        Perform attack
        """
        print(f"Attacking with strength: {self.strength}")

    def negotiate(self) -> None:
        """
        Perform attack
        """
        print(f"Negotiating with strength: {self.diplomacy}")

