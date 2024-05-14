import json
import google.generativeai as genai
import os
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.console import Console



def main():

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')


#         input = f"""
#         Generate 1 unique planet for a tabletop rpg. Answer in JSON format with primary keys: name, description, planet_type, items. 
#         For items, only generate a max of 3 items. Make sure the theme is science fiction.
# """

#         input = f"""
#         Generate 1 unique planet for a tabletop rpg. Answer in JSON format with primary keys: name, description, planet_type, items. 
#         For items, only generate a max of 3 items. Make sure the theme is science fiction Write the decription as though it is the beginning of an episode of TV.
# """       

        input = f"""
Pretend that we are writing a tv script for a science fiction show that involves exploring the final frontier. 
Our heroes spaceship, the USS Reliant has just entered the Kelvin system. Write three sentences that act as the intro line to the episode. 
Then write three sentences that act as the last few lines of episode summary told by a character at the end of the 45 min episode. 
Give the output as a JSON with primary keys: "intro_text", "outro_text".
        
"""


        response = model.generate_content(input,safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})

        print("RESPONSE TEXT------------------------")
        print(response.text)
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")
        finaltext = finaltext.replace("json", "")

        parsed_dict = {}
        try:
            parsed_dict = json.loads(finaltext)
            print("LOADED JSON------------------------")
            for k,v in parsed_dict.items():
                print(f"{k}\n")
                print(f"{v}\n")
        except:
            print("Could not load JSON.")

        console = Console()
        console.clear()
        console.rule("[bold red]Encounter Text:")

        intro_story_text = Text("Our story so far...\n", style="green")
        if "intro_text" in parsed_dict.keys():
            for text in parsed_dict["intro_text"]:
                intro_story_text.append(" "+text)

        intro_story_panel= Panel(intro_story_text, title="Intro")
        console.print(intro_story_panel)

        outro_story_text = Text("Finally...\n", style="green")
        if "outro_text" in parsed_dict.keys():
            for text in parsed_dict["outro_text"]:
                outro_story_text.append(" "+text)

        outro_story_panel= Panel(outro_story_text, title="Outro")
        console.print(outro_story_panel)



        # if "description" in parsed_dict:

        #     input = f"""My starship crew would like to investigate this planet more. It was the current description: 
        #     {parsed_dict['description']}. Please write an episode of TV that gives the begining of this journey. 
        #     Give the output in JSON format where primary keys correspond to the scene numbers. Also For example: scene_number. 
        #     Do not name the characters after famous celebrities. For each scene also generate a science fiction themed item that would be used in a tabletop card game."""

        #     response = model.generate_content(input,safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})

        #     print("RESPONSE TEXT------------------------")
        #     print(response.text)
        #     finaltext = response.text.replace("`", "")
        #     finaltext = finaltext.replace("python", "")
        #     finaltext = finaltext.replace("json", "")
        #     print("LOADED JSON------------------------")
        #     parsed_dict = json.loads(finaltext)
        #     for k,v in parsed_dict.items():
        #         print(f"{k}\n")
        #         print(f"{v}\n")



if __name__ == "__main__":
    main()