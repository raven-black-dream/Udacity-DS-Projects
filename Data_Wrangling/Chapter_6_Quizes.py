#Quiz 1

import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename, events = ["end"]):
        tag = elem.tag
        if tag not in tags:
            tags[tag] = 1
        else:
            tags[tag] += 1
    return tags

def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}



if __name__ == "__main__":
    test()

#Quiz 2
import re
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":

        print problemchars.findall(element.attrib['k'])
        if problemchars.findall(element.attrib['k']) != []:
            keys['problemchars'] += 1

        elif lower_colon.match(element.attrib['k']) != None:
            keys['lower_colon'] += 1

        elif lower.match(element.attrib['k']) != None:
            keys['lower'] += 1

        else: keys['other'] += 1

    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()

# Quiz 3
def get_user(element):
    tags = ["node", "way", "relation"]

    if element.tag in tags:
        return element.attrib['user']
    else:
        return None


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if get_user(element) != None:
            users.add(get_user(element))

    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()

#Quiz 4
from collections import defaultdict
OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd." : "Road",
            "Rd" : "Road",
            "Ave" : "Avenue",
            "Ave" : "Avenue"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                print tag.attrib
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    for key in mapping.keys():
        if name[m.start() : m.end()] == key:
            name = name[0 : m.start()] + mapping[key]
            print name

    return name


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()

#Quiz 5
import codecs
import json
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    attributes = element.attrib
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        for attribute in attributes:
            if attribute in CREATED:
                if not 'created' in node:
                    node['created'] = {}
                node['created'][attribute] = element.attrib[attribute]
            elif attribute == "lat" or attribute == "lon":
                if not 'pos' in node:
                    node['pos'] = []
                node['pos'].append(float(element.attrib[attribute]))
            else:
                node[attribute] = element.attrib[attribute]
        for tag in element.iter("tag"):
            if problemchars.search(tag.attrib['k']):
                continue
            elif tag.attrib['k'].count(':') == 2:
                continue
            elif tag.attrib['k'].startswith("addr:"):
                if not 'address' in node:
                    node['address'] = {}
                index = tag.attrib['k'].index(':')
                key = tag.attrib['k'][index + 1 : len(tag.attrib['k'])]
                node['address'][key] = tag.attrib['v']
            else:
                node[tag.attrib['k']] = tag.attrib['v']
        if element.tag == 'way':
            if not 'node_refs' in node:
                node['node_refs'] = []
            for nd in element.iter('nd'):
                node['node_refs'].append(nd.attrib['ref'])
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    print data[0]
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('example.osm', True)
    #pprint.pprint(data)

    assert data[0] == {
                        "id": "261114295",
                        "visible": "true",
                        "type": "node",
                        "pos": [
                          41.9730791,
                          -87.6866303
                        ],
                        "created": {
                          "changeset": "11129782",
                          "user": "bbmiller",
                          "version": "7",
                          "uid": "451048",
                          "timestamp": "2012-03-28T18:31:23Z"
                        }
                      }
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.",
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369",
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()