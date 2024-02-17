import os
import logging

try:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
except KeyError:
    logging.Logger.warn("NO GOOGLE API KEY!")
    GOOGLE_API_KEY = None

STAR_DIRECTORY = "starsystems"

PLANET_NOUNS =  ['planet', 'p', 'pl']
LEAVE_COMMANDS = ["l", "le", "leave"]
GET_COMMANDS = ["g", "get", "GET", "ge"]
SCAN_COMMANDS = ["sc", "scan"]

DIPLOMACY = "diplomacy"
STRENGTH = "strength"
SCIENCE = "science"

PLANET_TYPES = ["M-Class", "Desert", "Swamp", "Tundra", "Gas Giant", "Dwarf", "Dyson Sphere"]

CARD_TYPES = [DIPLOMACY, STRENGTH, SCIENCE]


ANOMALIES = [

"Wormholes",
"Black Holes",
"Dark Matter Singularity",
"Quantum Foam",
"Distress Signal",
"Ancient Probe",


]

CAPTAIN_QUIPS = ["Make it so.", "Punch it.", "Engage.", "Steady as she goes."]
