class Ship():
    """
    The main class that the ship, aka the PLAYER.
    """

    def __init__(self, name, location) -> None:
        """

        :param name:
        :param location: a StarSystem of Class StarSystem
        """

        # Load Model, feed it inputs and then generate items.


        self.name = name
        # Mars, Pluto, Alpha Centauri, Etc.
        self.location = location
        self.health = 100
        self.crew = 50
        self.strength = 80
        self.science = 80
        self.diplomacy = 80

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

