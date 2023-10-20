import yaml

with open("starsystems/starsystem.yaml", mode="rt", encoding="utf-8") as file:
    print(yaml.safe_load(file))