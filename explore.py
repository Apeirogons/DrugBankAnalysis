from parse_xml import *
from Drug import *

loc = "C:\\Users\\somat\\Downloads\\full database.xml"
_ = open(loc,encoding = "utf8")
a = _.read()
a = a.split("\n")

a = separate_by_drug(a)

drugs_library = []
print(create_drug_object(a[48]))

#    drugs_library.append(create_drug_object(x))



