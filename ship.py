# from collections.abc import MutableMapping
# from typing import Any
from constants import DIPLOMACY, STRENGTH, SCIENCE
from rich.table import Table

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

        #self.cargo.update({"Tribbles":"They don't do much, other than make more tribbles."})
        
        self.cargo.update({"Tribbles":{"desc":"They don't do much, other than make more tribbles.", "power_level": 2, "power_type": SCIENCE}})
        self.cargo.update({"Tea":{"desc":"Earl grey", "power_level": 2, "power_type": DIPLOMACY}})
        self.cargo.update({"Quantum Torpedos":{"desc":"Powerful torpedos", "power_level": 2, "power_type": STRENGTH}})

        self.max_cargo_size = 5
        self.cargo_size = len(self.cargo.keys())

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


def build_status_table(player_ship):
    table = Table(title=f"{player_ship.name.upper()} Status")

    table.add_column("Location", justify="right", style="cyan", no_wrap=True)
    table.add_column("Hull", style="magenta")
    table.add_column("Crew", justify="right", style="green")
    table.add_column("Strength", justify="right", style="cyan")
    table.add_column("Science", justify="right", style="magenta")
    table.add_column("Diplomacy", justify="right", style="green")
    table.add_column("Exp", justify="right", style="blue")
    table.add_column("Exp Nxt Lvl", justify="right", style="cyan")

    table.add_row(player_ship.location.name, str(player_ship.health), str(player_ship.crew), str(player_ship.strength), str(player_ship.science), str(player_ship.diplomacy), str(player_ship.experience), str(player_ship.exp_next_level))

    return table

def build_cargo_table(player_ship):
    table = Table(title=f"{player_ship.name.upper()} Cargo")
    table.add_column("Item", justify="right", style="cyan", no_wrap=True)
    table.add_column("Desc", style="green")
    table.add_column("Type", style="magenta")
    table.add_column("Power", style="yellow")

    for n,d in player_ship.cargo.items():
        table.add_row(str(n), str(d["desc"]), str(d["power_type"]),str(d["power_level"]) )

    return table