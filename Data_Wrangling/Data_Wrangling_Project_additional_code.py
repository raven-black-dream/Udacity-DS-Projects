
# coding: utf-8

# In[1]:

import codecs
import json
import pprint
import xml.etree.ElementTree as ET
import os
from collections import defaultdict
import re
import pprint

f = os.path.normpath('C:/Users/Evan/Downloads/victoria_canada.osm')
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    attributes = element.attrib
    if element.tag == "node" or element.tag == "way":
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
    context = ET.iterparse(file_in, events = ('start', 'end'))
    context = iter(context)
    event, root = context.next()
    file_out = "{0}.json".format(file_in)
    with codecs.open(file_out, "w") as fo:
        for event, element in context:
            if event == 'end':
                root.clear()
            else:    
                el = shape_element(element)
                if el:
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")


# In[2]:

process_map(f, False)


# In[1]:

import ast
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.osm
    return db


# In[28]:

import pprint
def make_pipeline():
    pipeline = [{'$match' : {'address.city' : {'$exists' : 1},
                             'address.street' : {'$exists' : 1}}},
                {'$group' : {'_id' : '$address.city',
                             'count' : {'$sum' : 1}}},
                {'$sort' : {'_id' : 1}}]
                
                
    return pipeline

def get_result(db, pipeline):
    result = db.victoria.aggregate(pipeline)
    return result

def foo(db, street_name):
    pipeline = [{'$match' : {'address.street' : street_name}},
                {'$project': {'number' : '$address.housenumber', 'street' : '$address.street'}},
                {'$sort' : {'street' : -1}}]
    result = db.victoria.aggregate(pipeline)
    return result
def get_fixed_city(street_names):
    victoria = [u'Durrance Close', u'Durrance Road', u'Helen Place', u'Willis Point Road']
    shirley = [u'Alderbrook Place', u'Denewood Place', u'Seaside Drive', u'Tieulie Place', u'Woodhaven Road']
    fixed_city = {}
    for i in range(len(street_names)):
        if street_names[i]['_id'] in victoria:
            fixed_city[street_names[i]['_id']] = 'Victoria'
        elif street_names[i]['_id'] in shirley:
            fixed_city[street_names[i]['_id']] = 'Shirley'
        elif street_names[i]['_id'] == u'West Coast Road':
            fixed_city[u'West Coast Road'] = 'Several'
        else:
            fixed_city[street_names[i]['_id']] = 'Sooke'
    return fixed_city

def fix_city_values(db, city_values):
    streets = city_values.keys()
    for street in streets:
        db.victoria.update({'address.city' : 'Capital H (Part 1)', 'address.street' : street},
                           {'$set' : {'address.city' : city_values[street]}},
                           multi = True)
    print 'Done'

if __name__ == '__main__':
    db = get_db()
    pipeline = make_pipeline()
    results = get_result(db, pipeline)
    results = results['result']
    #fixed_city_values = get_fixed_city(results)
    #fix_city_values(db, fixed_city_values)
    for result in results:
        pprint.pprint(result)
        #st_info = foo(db, result['_id'])
        #pprint.pprint(st_info['result'])
        


# In[3]:

db.victoria.update({'address.city' : u'Becher Bay 1'},
                   {'$set': {'address.city' : u'Sooke'}},
                   multi = True)


# In[4]:

db.victoria.update({'address.city' : u'Cole Bay 3'},
                   {'$set' : {'address.city' : u'North Saanich'}},
                   multi = True)


# In[5]:

db.victoria.remove({'address.city' : u'Coupeville'})


# In[6]:

db.victoria.remove({'address.city' : u'Ferndale'})


# In[7]:

db.victoria.remove({'address.city' : u'Friday Harbor'})


# In[9]:

db.victoria.update({'address.city' : u'Mayne'},
                   {'$set' : {'address.city' : u'Mayne Island'}},
                   multi = True)


# In[10]:

db.victoria.remove({'address.city' : u'Port Angeles'})


# In[27]:

db.victoria.update({'address.city' : u'Saturna'},
                   {'$set' : {'address.city' : u'Saturna Island'}},
                   multi = True)


# In[13]:

db.victoria.update({'address.city' : u"T'Sou-ke"},
                   {'$set' : {'address.city' : 'Sooke'}},
                   multi = True)


# In[15]:

db.victoria.update({'address.city' : u'Union Bay 4'},
                   {'$set' : {'address.city' : 'Union Bay'}},
                   multi = True)


# In[25]:

query = {'address.city' : 'Several'}
projection = {'_id': 0, 'address.housenumber' : 1}
west_coast_road = db.victoria.find(query, projection)
for address in west_coast_road:
    if int(address['address']['housenumber']) < 10000:
        db.victoria.update({'address.street': u'West Coast Road', 'address.housenumber': address['address']['housenumber']},
                           {'$set': {'address.city' : u'Sooke'}})
    elif int(address['address']['housenumber']) == 10018:
        db.victoria.update({'address.street': u'West Coast Road', 'address.housenumber': address['address']['housenumber']},
                           {'$set': {'address.city' : u'Shirley'}})
    else:
        db.victoria.update({'address.street': u'West Coast Road', 'address.housenumber': address['address']['housenumber']},
                           {'$set': {'address.city' : u'Port Renfrew'}})
print "done"


# In[ ]:



