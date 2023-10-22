import yaml
from datetime import datetime
from rich import print

def load_model():

    #loading model and generating output may take a bit, so we should put a loading icons somewhere.

    return 0

def prompt_model():

    model_output = "No output yet."

    return model_output

def load_starsystem_yaml() -> dict:


    with open("starsystems/starsystem.yaml", mode="rt", encoding="utf-8") as file:
        # print("\n")
        # print(yaml.safe_load(file))
        all_starsystems = yaml.safe_load(file)
        for k,v in all_starsystems.items():
            print("\n")
            print(k)
            print(v)
        print(type(all_starsystems))
        print(datetime.now())

    

    return all_starsystems