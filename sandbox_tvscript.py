import json
import google.generativeai as genai
import os


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

        input = f"""
        Generate 1 unique planet for a tabletop rpg. Answer in JSON format with primary keys: name, description, planet_type, items. 
        For items, only generate a max of 3 items. Make sure the theme is science fiction Write the decription as though it is the beginning of an episode of TV.
"""       

        response = model.generate_content(input,safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})

        print("RESPONSE TEXT------------------------")
        print(response.text)
        finaltext = response.text.replace("`", "")
        finaltext = finaltext.replace("python", "")
        finaltext = finaltext.replace("json", "")

        try:
            parsed_dict = json.loads(finaltext)
            print("LOADED JSON------------------------")
            for k,v in parsed_dict.items():
                print(f"{k}\n")
                print(f"{v}\n")
        except:
            print("Could not load JSON.")

        
        if "description" in parsed_dict:

            input = f"""My starship crew would like to investigate this planet more. It was the current description: 
            {parsed_dict['description']}. Please write an episode of TV that gives the begining of this journey. 
            Give the output in JSON format where primary keys correspond to the scene numbers. Also For example: scene_number. 
            Do not name the characters after famous celebrities. For each scene also generate a science fiction themed item that would be used in a tabletop card game."""

            response = model.generate_content(input,safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_ONLY_HIGH'})

            print("RESPONSE TEXT------------------------")
            print(response.text)
            finaltext = response.text.replace("`", "")
            finaltext = finaltext.replace("python", "")
            finaltext = finaltext.replace("json", "")
            print("LOADED JSON------------------------")
            parsed_dict = json.loads(finaltext)
            for k,v in parsed_dict.items():
                print(f"{k}\n")
                print(f"{v}\n")



if __name__ == "__main__":
    main()