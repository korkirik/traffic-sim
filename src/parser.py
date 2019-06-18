import json

with open('export_map_data.json', 'r') as export:
    meta_data = json.load(export)


number_of_elements = 5 #len(meta['features'])

for i in range(0, number_of_elements):
    geometry = meta_data['features'][i]['geometry']
    if geometry['type'] == 'LineString':
        properties = meta_data['features'][i]['properties']
        highway = properties['highway']
        #print(type(highway))
        print(highway)
        name = properties['name']
        print(name)
        lanes = properties['lanes']
        print(lanes)
        print("\n")


export.close()