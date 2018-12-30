# detects the number of spaces before a string.
def detect_level(string):
    n_spaces = 0
    for char in string:
        if char == " ":
            n_spaces += 1
        else:
            break
    return n_spaces


# gets all strings on a level. Not useful.
def get_strings_on_level(newline_strings, n):
    strings_on_level = []
    for string in newline_strings:
        if detect_level(string) == n:
            strings_on_level.append(string)
    return strings_on_level


# Returns content within a single-line tag. Otherwise, returns False
def detect_single_line_tag(line, tag_name):
    entry_tag = "<" + tag_name + ">"
    location_of_entry_tag = line.find(entry_tag)

    if location_of_entry_tag == -1:
        return False
    else:
        closing_tag = "</" + tag_name + ">"
        location_of_closing_tag = line.find(closing_tag)
        if location_of_closing_tag == -1:
            return False
        else:
            return line[location_of_entry_tag + len(entry_tag):location_of_closing_tag]


# Searches for the start point of a drug name, part of the next function
def _search_drug_start(newline_strings, drug_name):
    for index, string in enumerate(newline_strings):
        if detect_single_line_tag(string, "name") == drug_name:
            if detect_level(string) == 2:
                return index-3
    return -1


# Searches the data of a drug from newline strings, useful for debugging
def search_drug(newline_strings, drug_name):
    drug_start = _search_drug_start(newline_strings, drug_name)
    assert drug_start != -1
    for index, string in enumerate(newline_strings[drug_start:]):
        if string == "</drug>": #note, this means that the string is on level 0
            return newline_strings[drug_start:index+drug_start]


# Part of the detect_multiline_tag function.
def detect_tag_location(newline_strings, tag, start_index):
    index_of_tag = start_index
    changed = False
    for index, string in enumerate(newline_strings[start_index:]):
        if string.find(tag) != -1:
            index_of_tag = index+start_index
            changed = True
            break
    if changed:
        return index_of_tag
    else:
        return -1


#  Gets all newline strings contained within a multi-line tag as the first return,
#  the second return being the line which the closing tag is on.

def detect_multiline_tag(newline_strings, tag_name, start_index = 0):
    entry_tag = "<" + tag_name + ">"
    closing_tag = "</" + tag_name + ">"
    entry_location = detect_tag_location(newline_strings, entry_tag, start_index)
    closing_location = detect_tag_location(newline_strings, closing_tag, start_index)

    if not (entry_location == -1 or closing_location == -1):
        return newline_strings[entry_location+1:closing_location], closing_location
    else:
        return -1, -1


# Gets all multi line tags of a particular type
def detect_all_multiline_tags(newline_strings,tag_name,start_index=0):
    tags = []
    i = start_index
    while True:
        tag_info, new_start_index = detect_multiline_tag(newline_strings,tag_name,i)
        if tag_info != -1:
            tags.append(tag_info)
            i = new_start_index +1
        else:
            break
    return tags


#Splits the dataset into data for different drugs.
def separate_by_drug(newline_strings):
    drugs = []
    start_of_drug = -1

    for index, string in enumerate(newline_strings):
        if string.find("drug type") != -1:
            start_of_drug = index
        elif string == "</drug>":
            end_of_drug = index
            drugs.append(newline_strings[start_of_drug:end_of_drug+1])

    return drugs


# Utility function to print a list on separate lines.
def sequential_print_list(list):
    for x in list:
        print(x)