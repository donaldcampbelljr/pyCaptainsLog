# import json
import google.generativeai as genai
import os
from random_generators import generate_planet_information
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich import print
from rich.console import Console
from main import parse_user_input
#
def main():

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    planet_name = "Tau Ceti"

    dict = generate_planet_information(planet_name)
    console = Console()
    console.clear()
    console.print("\n")
    console.rule(f"\n[bold red]System: {planet_name} Planet: {planet_name}")
    player_input = None
    while player_input != 'leave':
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="middle"),
            Layout(name="lower")
        )

        layout["lower"].ratio = 2
        layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="middle1"),
            Layout(name="middle2"),
            Layout(name="right"),
        )

        if "name" in dict:
            upper_text = Text(f"You've entered into orbit of the planet {planet_name}\n", style="cyan3")
        if "description" in dict:
            upper_text.append(dict["description"]+"\n", style="dark_turquoise")

        if upper_text is None:
            upper_text = Text(f"You've entered the orbit of an unknown planet.")

        layout["upper"].update(upper_text)

        item_titles = []
        item_descs = []
        item_type = []
        if "items" in dict:
            items_text = Text("")
            # for i in dict["items"]:
            if isinstance(dict["items"], list):
                for item in dict["items"]:
                    if "name" in item:
                        items_text.append(item["name"] + "\n")
                        # also want to make a lowercase version of the name for picking up
                        lc_name = item["name"].lower()
                        lc_name = lc_name.replace(" ", "")
                        item["lcname"] = lc_name
                        item_titles.append(item["name"])
                        item_descs.append(item["description"])
        else:
            items_text = Text("no items")

        item_type = ['science    +5', 'combat    +4', 'diplomacy    +7']

        command_text = Text("LEAVE ORBIT: `leave`\n", style="deep_pink1")
        command_text.append("GET ITEM: `get xxxxx`", style="bright_cyan")

        layout["left"].update(
            Panel(item_descs[0], title=item_titles[0], subtitle=item_type[0])
        )
        layout["middle1"].update(
            Panel(item_descs[1], title=item_titles[1], subtitle=item_type[1])
        )

        layout["middle2"].update(
            Panel(item_descs[2], title=item_titles[2], subtitle=item_type[2])
        )

        layout["right"].split(
            Layout(Panel(items_text, title="UPCOMING ITEMS")),
            Layout(Panel(command_text, title="COMMANDS"))
        )

        print(layout)

        player_input = input("Your Orders, Captain? > ")
        verb, noun, extra = parse_user_input(player_input)

        LEAVE_COMMANDS = ["l", "le", "leave"]
        GET_COMMANDS = ["g", "get", "GET", "ge"]
        if verb in LEAVE_COMMANDS:
            console.clear()
            console.print("[bold red]Leaving Orbit...")
            input("> ")
            break


if __name__ == "__main__":
    main()
