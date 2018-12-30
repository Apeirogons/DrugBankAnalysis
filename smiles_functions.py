def element_detector(molecule):
    element_map = []

    while len(molecule) > 0:
        if molecule[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if len(molecule) > 1:
                if molecule[1] in "abcdefghijklmnopqrstuvwxyz":
                    fragment_size = 2
                else:
                    fragment_size = 1
            else:
                fragment_size = 1
        else:
            fragment_size = 1
        element_map.append(molecule[0:fragment_size])
        molecule = molecule[fragment_size:]

    return element_map


def bracket_forge(molecule):
    element_map = []

    while len(molecule) > 0:
        if molecule[0] == "[":
            location_of_closing = molecule.index("]")
            element_map.append("".join(molecule[0:location_of_closing + 1]))
            fragment = location_of_closing + 1
        else:
            element_map.append(molecule[0])
            fragment = 1
        molecule = molecule[fragment:]
    return element_map


def create_unique_chars_histogram(small_molecules):
    unique_characters = []
    for molecule in small_molecules:
        for char in bracket_forge(element_detector(molecule.lookup_attr("SMILES"))):
            found_char = False
            for i, base_characters in enumerate(unique_characters):
                if char == base_characters[0]:
                    unique_characters[i][1] += 1
                    found_char = True
                    break
            if not found_char:
                unique_characters.append([char, 1])

    unique_characters = sorted(unique_characters, key=lambda x: x[1])
    unique_characters.reverse()

    return unique_characters


def clean_molecules_using_histogram(small_molecules, unique_characters, n=30):
    cleaned_small_molecules = []
    for index, mol in enumerate(small_molecules):

        mol_OK = True
        for char in bracket_forge(element_detector(mol.lookup_attr("SMILES"))):
            char_OK = False
            for master_char in unique_characters[:n]:
                if char == master_char[0]:
                    char_OK = True
                    break
            if not char_OK:
                mol_OK = False
                break
        if mol_OK:
            cleaned_small_molecules.append(mol)
    return cleaned_small_molecules


