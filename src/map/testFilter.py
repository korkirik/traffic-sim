import json

with open('export_json_filtered.json', 'r') as test:
    obj = json.load(test)

#for street_name in obj
 #   street_name = obj["@user"]
#    print("\n" + street_name)

features = obj["features"]
properties = obj.features.properties #dict(features[1])

print(properties)
#properties = dict(features["properties"])
#highway = dict(properties["highway"])
#      [properties[highway]])
#print(highway)
test.close()