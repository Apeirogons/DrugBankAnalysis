from parse_xml import detect_single_line_tag, detect_all_multiline_tags, detect_multiline_tag
from handle_water_solubility import handle_water_solubility



def attributes_from_multiline(multiline_properties):
    if multiline_properties == -1:
        return []
    attributes = []
    field_tags = ["kind", "value", "source"]
    collected_properties = detect_all_multiline_tags(multiline_properties, "property")

    for index,property in enumerate(collected_properties):
        property_length = len(property)

        # sometimes, the source lines are too long. here's some code to remedy this
        if property_length > 3:
            n_too_much = property_length - 3
            # add the extra lines onto the source line
            for i in range(1, n_too_much+1):
                collected_properties[index][2] += collected_properties[index][2+i]
            # delete the extra lines
            for i in range(n_too_much):
                collected_properties[index].remove(property[3])

        # I'd be very confused if there was still bugs here.
        if len(property) == 3:
            obtained_data = [detect_single_line_tag(field, field_tags[i]) for i, field in enumerate(property)]
            attributes.append(Attribute(obtained_data[0], obtained_data[1], obtained_data[2]))
        else:
            print(property)
            print("Property length invalid: " + str(len(property)))
            raise Exception

    return attributes


def create_drug_object(drug_multiline):
    calc_properties = attributes_from_multiline(detect_multiline_tag(drug_multiline, "calculated-properties")[0])
    exp_properties = attributes_from_multiline(detect_multiline_tag(drug_multiline, "experimental-properties")[0])
    atc_code_line = detect_multiline_tag(drug_multiline, "atc-codes")[0]

    if atc_code_line != -1:
        atc_code = atc_code_line[0][20:27]
    else:
        atc_code = "XNoData"

    _ = drug_multiline[0]
    drug_type = _[12:_.find('"', 12)]

    for index, string in enumerate(drug_multiline):
        potential_name = detect_single_line_tag(string, "name")
        if potential_name != False:
            name = potential_name
            break

    return Drug(name, atc_code, drug_type, calc_properties, exp_properties)


class Attribute(object):
    def __init__(self, kind, value, source = None):
        self.kind = kind
        self.source = source

        if self.kind == "Water Solubility":
            self.value = handle_water_solubility(value)
            self.numeric = True
        else:
            try:
                self.value = float(value)
                self.numeric = True
            except ValueError:
                self.value = value
                self.numeric = False

    def __str__(self):
        return self.kind + " " + str(self.value)


class Drug(object):
    def __init__(self, name, atc_code, drug_type,  calc_attributes, exp_attributes):
        self.name = name
        self.atc_code = atc_code
        self.drug_type = drug_type
        self.attributes = []
        self.overwrite_attributes(calc_attributes)
        self.overwrite_attributes(exp_attributes)

    @staticmethod
    def _group_attributes(attributes):
        attributes_groupings = []
        for attr in attributes:
            should_add_new_attribute = True
            for attr_grouping in attributes_groupings:
                if attr.kind == attr_grouping[0]:
                    attr_grouping[1].append(attr)
                    should_add_new_attribute = False
                    break

            if should_add_new_attribute:
                attributes_groupings.append([attr.kind, [attr]])
        return attributes_groupings

    @staticmethod
    def merge_attributes(attributes):
        merged_attributes = []
        attributes_groupings = Drug._group_attributes(attributes)
        for attribute_group in attributes_groupings:
            attribute_instances = len(attribute_group[1])
            if attribute_instances == 1:
                processed_attribute = attribute_group[1][0]

            elif attribute_instances > 1:
                numeric_merged_value = 0
                n_numeric_instances = 0
                for attribute in attribute_group[1]:
                    if attribute.numeric:
                        n_numeric_instances += 1
                        numeric_merged_value += attribute.value

                average_numeric = numeric_merged_value/n_numeric_instances
                processed_attribute = Attribute(attribute_group[0], average_numeric, source = "merged")

            merged_attributes.append(processed_attribute)
        return merged_attributes

    def overwrite_attributes(self, attributes):
        merged_attributes = Drug.merge_attributes(attributes)
        for new_attr in merged_attributes:
            should_add_this_attr = True
            for index, old_attr in enumerate(self.attributes):
                if old_attr.kind == new_attr.kind and new_attr.numeric:
                    self.attributes[index] = new_attr
                    should_add_this_attr = False
                    break
            if should_add_this_attr:
                self.attributes.append(new_attr)

    def lookup_attr(self, attr_kind):
        for attr in self.attributes:
            if attr_kind == attr.kind:
                return attr.value
        else:
            return "No Data"

    def __str__(self):
        return self.name + " " + self.atc_code + " " + self.drug_type + " " + str([str(attr) for attr in self.attributes])
