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


        self.name = "USS Fed Star Ship"
        # Mars, Pluto, Alpha Centauri, Etc.
        self.location = location

        pass

    def scan(self) -> None:
        """
        "Scan" the system, read the system info to the player.
        """
        print(self.location.info)
