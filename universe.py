import os
from os import walk, path
from os import system, name
from constants import STAR_DIRECTORY
import pandas as pd

from starsystem import load_starsystem_yaml


def universe_save():
    list_systems = []
    path_starsystems = os.path.abspath(STAR_DIRECTORY)
    for (dirpath, dirnames, filenames) in walk(path_starsystems):
        print("Collecting filenames")
        for file in filenames:
            system = load_starsystem_yaml(file)
            list_systems.append(system)

    # Convert list of dicts to a dataframe
    system_df = pd.DataFrame(list_systems)

    link = os.path.abspath(STAR_DIRECTORY)+"universe.csv"
    #save to the star directory
    system_df.to_csv(link, index=True)

    return link