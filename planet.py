import random

import yaml
import os
from os import walk
from os import system, name
from constants import STAR_DIRECTORY
from random_generators import (
    generate_system_name,
    generate_alien_name,
    generate_planets_list,
    get_intro_text,
)
from rich import print
from rich.console import Console


class Planet:
    """
    The main class that initializes planet
    """

    def __init__(
        self, name, alien, intro_text, events,
    ) -> None:

        # Load Model, feed it inputs and then generate items.

        self.name = name
        self.alien = alien
        self.intro_text = intro_text
        name = name.replace(" ", "")
        name = name.lower()
        # Make the string lowercase using th

        self.events = events

    def __str__(self):
        return f"Planet {self.name}"
