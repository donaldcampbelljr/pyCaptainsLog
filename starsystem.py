import yaml
import os
from constants import STAR_DIRECTORY

class StarSystem():
    """
    The main class that intializes star systems and is populated with attributes (planets, etc).
    """

    def __init__(self, name, planets, alien, linked_systems, intro_text) -> None:

        # Load Model, feed it inputs and then generate items.

        self.name = name
        self.planets = planets
        self.alien = alien
        self.linked_systems = linked_systems
        self.intro_text = intro_text

        # self.name = "DefaultSystemName"
        # # Mars, Pluto, Alpha Centauri, Etc.
        # self.planets = ["Earth", "Mars", "Pluto"]
        #
        # # Klingons, Killer Robots, etc.
        # self.alien = "DefaultAlienName"
        #
        # self.linked_systems = ["origin1"]
        #
        # self.intro_text = f"Welcome to the {self.name} system!"


    def __str__(self):
        return f"Starsystem {self.name}"



def save_star_system(starsystem):
    # I thought it would be nice to have all star systems in one big yaml.
    # But maybe it is best to have them segregated such that the info is easier to read.

    starsystem_dict = {}

    # This is clunky, should just make StartSystem class a MutableMapping that has keys...
    if starsystem.name:
        starsystem_dict.update({"StarSystemName": starsystem.name})
    if starsystem.planets:
        starsystem_dict.update({"planets": starsystem.planets})
    if starsystem.alien:
        starsystem_dict.update({"alien": starsystem.alien})
    if starsystem.linked_systems:
        starsystem_dict.update({"linked_systems": starsystem.linked_systems})
    if starsystem.intro_text:
        starsystem_dict.update({"intro_text": starsystem.intro_text})

    yaml_obj_to_write = yaml.dump(starsystem_dict)

    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    # This is incorrect syntax for appending filename to path as a file in the directory: os.path.join(path_starsystems + file_name)
    file_name = starsystem.name + ".yaml"

    file_path = os.path.join(path_starsystems , file_name)

    with open(file_path, 'w',) as f :
        f.write(yaml_obj_to_write)
    
    print("\n Successful Save to File")


    return 0

def create_starsystem():

    starsystem = StarSystem()

    return starsystem

def jump_to_starsystem(current_system, next_system):

    ## Check if ship location is already at system
    # check if starsystem already exists (the yaml)
    # create new star system as last option.
    print(f"Current System: {current_system}\n")
    print(f"Next System: {next_system}\n")

    # read files from
    from os import walk
    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    filenames = []
    for (dirpath, dirnames, filenames) in walk(path_starsystems):
        print(filenames)

    if current_system.name == next_system:
        print("You are already in this system.")

    if next_system in filenames:
        load_starsystem_yaml(next_system)
    else:
        # Now we should create a new star system:
        create_starsystem()
    return 0


def load_starsystem_yaml(starsystemname) -> dict:


    path_starsystems =  os.path.abspath(STAR_DIRECTORY)
    # This is incorrect syntax for appending filename to path as a file in the directory: os.path.join(path_starsystems + file_name)
    file_name = starsystemname + ".yaml"

    file_path = os.path.join(path_starsystems , file_name)
    with open(file_path, mode="rt", encoding="utf-8") as file:
        # print("\n")
        # print(yaml.safe_load(file))
        starsystem_loaded = yaml.safe_load(file)
        for k,v in starsystem_loaded.items():
            print("\n")
            print(k)
            print(v)


    return starsystem_loaded