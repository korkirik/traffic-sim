import json

with open('export_map_data.json', 'r') as export:
    meta_data = json.load(export)


number_of_elements = 5#len(meta_data['features'])

for i in range(0, number_of_elements):
    geometry = meta_data['features'][i]['geometry']
    if geometry['type'] == 'LineString':
        properties = meta_data['features'][i]['properties']

        highway = properties.get('highway','Street')
        #print(type(highway))
        print(highway)
        name = properties.get('name','Street name')

        print(name)
        lanes = int(properties.get('lanes','1'))

        print(lanes)
        #print(type(lanes))
        print("\n")

        startXcoor = geometry['coordinates'][0][0]
        print(startXcoor)
        print(type(startXcoor))

        startYcoor = geometry['coordinates'][0][1]
        print(startYcoor)
        print(type(startYcoor))

        endXcoor = geometry['coordinates'][-1][0]
        print(endXcoor)
        print(type(endXcoor))

        endYcoor = geometry['coordinates'][-1][1]
        print(endYcoor)
        print(type(endYcoor))


export.close()