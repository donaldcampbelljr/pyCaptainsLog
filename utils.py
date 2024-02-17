
def parse_user_input(input):
    # simple verb noun identifier
    # e.g. explore planet planet a
    user_input = input.split()
    user_input = map(str.strip, user_input)
    user_input = list(user_input)

    try:
        verb = user_input[0]
    except IndexError:
        verb = None

    try:
        noun = user_input[1]
    except IndexError:
        noun = None

    try:
        extra = user_input[2:]
        if len(extra)>1:
            extra = ' '.join(extra) # if the name the user gives is 2 or more words...
        #     extra.lower() # lowercase so that all proper names have no spaces and
        elif len(extra) == 1:
            extra = extra[0].lower()
        # else:
        #     extra = None
    except IndexError:
        extra = None

    return verb, noun, extra