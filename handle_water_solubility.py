

# Water solubility isn't standardized for some reason. Need to fix this.
# Returns water solubility in g/L, or -1 if invalid
def handle_water_solubility(attribute_string):

    # Apparently, some solubility has no units and was auto-converted to float. No units is a problem
    if type(attribute_string) != str:
        return -1

    # Clip the attribute string until there's a number. If there's no numbers, there's a problem.
    while attribute_string[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        attribute_string = attribute_string[1:]
        if len(attribute_string) == 0:
            return -1

    # If there's no units, there's a problem.
    unit_slash = attribute_string.find("/")
    if unit_slash == -1:
        return -1

    # code to find the units
    first_space = attribute_string.find(" ")
    unit_numerator = attribute_string[first_space+1:unit_slash].lower()
    unit_denominator_end = attribute_string.find(" ", unit_slash)

    if unit_denominator_end == -1:
        unit_denominator_end = len(attribute_string)

    unit_denominator = attribute_string[unit_slash+1:unit_denominator_end].lower()

    # unit conversions
    multiplier = 1
    if unit_numerator == "g":
        multiplier *= 1
    elif unit_numerator == "mg":
        multiplier *= 1e-3
    elif unit_numerator == "kg":
        multiplier *= 1e3
    else:
        return -1

    if unit_denominator == "l":
        multiplier /= 1
    elif unit_denominator == "ml":
        multiplier /= 1e-3
    elif unit_denominator == "dl":
        multiplier /= 1e-1
    else:
        return -1

    # code to "deal" with numeric ranges -
    # and by that, I mean ignore them because I don't really want to write code for maybe 10 drugs

    numeric_value = attribute_string[:first_space]

    try:
        solubility = float(numeric_value) * multiplier
    except ValueError:
        return -1

    return solubility
