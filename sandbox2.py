# import json
import google.generativeai as genai
import os

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from random_generators import generate_planet_information, generate_generic_event
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich import print
from rich.console import Console
from main import parse_user_input
from ship import *
from starsystem import *
#
def main():

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        raise KeyError
    

    def get_gemini_reponse(input):
        #response = chat.send_message(input,stream=False, safety_settings={'HARM_CATEGORY_HARASSMENT':'block_none'})

        ## this allows us to have combat without tripping the safety mechanism,e.g. "Fire all phasers!" would sometimes trigger it.
        response = chat.send_message(input, stream=False,
                                        safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})


        return response
    
#     initial_input = """
# Pretend you are an enemy alien engaged with my ship in combat. I will play cards that deel specific types of damage.
# """
    
        # This is a combat mission example using cards (items) that the ship has gained.
    starting_location = load_starsystem_yaml("sol.yaml")
    starting_location = create_starsystem_from_dict(starting_location)

    current_system = starting_location
    ship = Ship(name="Reliant", location=current_system)

    planet_name = "Tau Ceti"

    planet_dict = generate_planet_information(planet_name)

    spawned_event = generate_generic_event()

    health  = ship.health
    enemy_health = 5

    initial_input = (f"Let us roleplay. I am a Captain of the {ship.name} on a mission of combat in the System {planet_name}."
                     f"You should pretend you are a hostile Alien in the {planet_name}. My ship has {health} health. Your alien ship has {enemy_health} health."
                     f"Please keep all responses to 2 sentences maximum. Every time I play card (starting with the next turn) I want you to narrate the battle.")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    response = get_gemini_reponse(initial_input)
    event_text = response.text

    console = Console()
    console.clear()
    console.print("\n")
    console.rule(f"\n[bold red]System: {planet_name} Planet: {planet_name}")
    
    #player_ship.cargo.update({item['name']:desc})


    player_input = None
    selection = None
    while player_input != 'leave':
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="middle"),
            Layout(name="lower")
        )

        layout["middle"].split_row(Layout(name="middleleft"),Layout(name="middleright"),)

        layout["middleleft"].ratio = 2

        #if selection is None:
        selection = event_text   

        spawned_event_text = Text(selection)

        layout["middleleft"].update(
            Panel(spawned_event_text, title="EVENT", subtitle="Combat")
        )

        layout["lower"].ratio = 2
        layout["lower"].split_row(
            Layout(name="left"),
            Layout(name="middle1"),
            Layout(name="middle2"),
            Layout(name="right"),
        )

        if "name" in planet_dict:
            upper_text = Text(f"You've entered into orbit of the planet {planet_name}", style="cyan3")
        if "description" in planet_dict:
            upper_text.append(planet_dict["description"]+"\n", style="dark_turquoise")

        if upper_text is None:
            upper_text = Text(f"You've entered the orbit of an unknown planet.")

        layout["upper"].update(upper_text)

        job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        task1 = job_progress.add_task("[green]Health", total=2)
        task2 = job_progress.add_task("[magenta]Crew", total=2)
        task3 = job_progress.add_task("[cyan]Science", total=2)

        job_progress.update(task1, advance=1)
        job_progress.update(task2, advance=0.5)
        job_progress.update(task3, advance=0.9)

        # total = sum(task.total for task in job_progress.tasks)
        # overall_progress = Progress()
        # overall_task = overall_progress.add_task("All Jobs", total=int(total))

        layout["middleright"].update(
            Panel(job_progress, title="test", subtitle="test")
        )


        # if "items" in planet_dict:
        #     items_text = Text("")
        #     # for i in dict["items"]:
        #     if isinstance(dict["items"], list):
        #         for item in dict["items"]:
        #             if "name" in item:
        #                 items_text.append(item["name"] + "\n")
        #                 # also want to make a lowercase version of the name for picking up
        #                 lc_name = item["name"].lower()
        #                 lc_name = lc_name.replace(" ", "")
        #                 item["lcname"] = lc_name
        #                 item_titles.append(item["name"])
        #                 item_descs.append(item["description"])
        # else:
        #     items_text = Text("no items")

        cards = generate_cards_dumb()

        # card_keys = list(cards.keys())
        # card_desc = list(cards.values())
        card_types = ['science', 'combat', 'diplomacy']

        item_titles = []
        item_descs = []
        item_type = []
        item_power = []

        for i in range(6):
            key, val = random.choice(list(cards.items()))
            item_titles.append(key)
            item_descs.append(val)
            item_type.append(random.choice(card_types))
            item_power.append(random.randint(1,7))

        command_text = Text("LEAVE ORBIT: `leave`\n", style="deep_pink1")
        command_text.append("USE CARD: `#1 or #2 or #3`", style="bright_cyan")

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
            Layout(Panel(str(item_titles[3]), title="UPCOMING ITEMS")),
            Layout(Panel(command_text, title="COMMANDS"))
        )

        print(layout)

        player_input = input("Your Orders, Captain? > ")
        verb, noun, extra = parse_user_input(player_input)

        LEAVE_COMMANDS = ["l", "le", "leave"]
        GET_COMMANDS = ["g", "get", "GET", "ge"]
        # for job in job_progress.tasks:
        #     if not job.finished:
        #         job_progress.advance(job.id)

        if verb in LEAVE_COMMANDS:
            console.clear()
            console.print("[bold red]Leaving Orbit...")
            input("> ")
            break
        try:
            sel = int(verb)

            if sel <= len(item_titles):
                # "use card"
                console.clear()
                console.print(f"Using {item_titles[sel]}")

                response = get_gemini_reponse(f"I play this card: {item_titles[sel]} with info {item_descs[sel]} and power {item_type[sel]} {item_power[sel]}. Narrate how this affects the battle.")
                event_text = response.text
        except:
            pass

def generate_cards_dumb():

    items = {}
    items.update({"Biomod Printer":"Prints and installs custom biological modifications."})
    items.update({"Zero-Point Converter":"Harnesses energy between dimensions, granting temporary power with unpredictable consequences."})
    items.update({"Sentient Holotape":"Data storage containing a digitized consciousness, eager to share forbidden knowledge."})
    items.update({"Stasis Grenade":"Suspends objects and people in frozen time for tactical escapes or interrogations."})
    items.update({"Neural Weaver":"Helmet for telepathic communication and manipulation, risking permanent consciousness merging."})
    items.update({"Gene Weaver Serum":"Grants temporary access to alien abilities at the cost of potential side effects."})
    items.update({"Quantum Compass":"Points to probabilities or potential futures, guiding through uncertain choices."})

    return items


if __name__ == "__main__":
    main()
