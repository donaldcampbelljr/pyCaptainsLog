import yaml
from datetime import datetime
from rich import print
from model_loading import load_starsystem_yaml
from starsystem import save_star_system
from starsystem import StarSystem


def main():

    # Initialize Game

    # Do a loading screen, basically ask the user if they are ready to load the galaxy?

    star_systems = load_starsystem_yaml()

    new_system = StarSystem()

    print(new_system.name)
    
    save_star_system(new_system)

    return 0

if __name__ == "__main__":
    main()