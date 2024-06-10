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


class Event:
    """
    Events are tied to a planet or a system.

    """

    def __init__(self, id, name, type, intro_text) -> None:

        # Load Model, feed it inputs and then generate items.

        self.id = id
        self.name = name
        self.type = type
        self.intro_text = intro_text
        name = name.replace(" ", "")
        name = name.lower()

    def __str__(self):
        return f"Event {self.name}"
