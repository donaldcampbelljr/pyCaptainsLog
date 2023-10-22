import model_loading
import yaml
import os
from constants import STAR_DIRECTORY

class StarSystem:
    """
    The main class that intializes star systems and is populated with attributes (planets, etc).
    """

    def __init__(self) -> None:

        # Load Model, feed it inputs and then generate items.


        self.name = "DefaultSystemName"
        # Mars, Pluto, Alpha Centauri, Etc.
        self.planets = ["Earth", "Mars", "Pluto"]

        # Klingons, Killer Robots, etc.
        self.alien = "DefaultAlienName"


        pass

    def __str__(self):
        return f"Starsystem {self.name}"



def save_star_system(starsystem):
    # I thought it would be nice to have all star systems in one big yaml.
    # But maybe it is best to have them segregated such that the info is easier to read.

    yaml_obj_to_write = yaml.dump(starsystem)
    path_starsystems = os.path.abspath(STAR_DIRECTORY)
    dir_name = os.path.dirname(path_starsystems)
    print(dir_name)
    print(path_starsystems)
    file_name = starsystem.name + ".yaml"
    print(file_name)
    # file_path = os.path.join(path_starsystems + str(os.sep()) + file_name)
    # print(file_path)


    return 0

