import random
import os
import google.generativeai as genai

def generate_system_name():
    first_syllables = ["Exo", "Aeth", "Xan", "Sol", "Terra", "Bel", "Mar", "Jov", "Neb", "Kep"]
    second_syllables = ["on", "ar", "eth", "ia", "us", "a", " Prime", " Major", " Minor", " Beta"]
    third_syllables = ["is", "os", "a", "or", "on", "ia", " Prime", " Major", " Minor", " Beta"]
    first = random.choice(first_syllables)
    second = random.choice(second_syllables)
    third = random.choice(third_syllables)
    return f"{first}{second}{third}"

def generate_alien_name():
    first_syllables = ["Zyl", "Xheth", "Yth", "Qel", "Vry", "T'eyl", "Khel", "Aethel", "Xylos", "Zyron"]
    second_syllables = ["an", "ar", "en", "in", "ai", "ora", "ryn", "thal", "kar", "nar"]
    third_syllables = ["'ai", "ath", "na", "on", "ya", "ee", "is", "kar", "van", "yr"]
    first = random.choice(first_syllables)
    second = random.choice(second_syllables)
    third = random.choice(third_syllables)
    return f"{first}{second}{third}"

def generate_planets_list():
    list_of_planets = []
    for i in range(random.randint(0, 5)):
        system_name = generate_system_name()
        list_of_planets.append(system_name)
    return list_of_planets

def get_intro_text(system_name):

    # First see if the Google API Key is available, else, generate some random text

    GOOGLE_API_KEY = None
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    except KeyError:
        print("None")

    if GOOGLE_API_KEY is not None:
        print("JUMPING INTO THE UNKNOWN....\n")
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro')

        response = model.generate_content(f"Write a brief description about the fictional {system_name} star system. Keep it to two lines of text."
                                          )
        ##print(to_markdown(response.text))
        ##print(response.text)
        intro_line = response.text
    else:
        def random_line(filename):
            """Reads a random line from a text file."""
            with open(filename, 'r') as file:
                lines = file.readlines()
                random_line = random.choice(lines)
                return random_line.strip()

        # Example usage:
        filename = "demo/infos.txt"
        intro_line = random_line(filename)

    return intro_line