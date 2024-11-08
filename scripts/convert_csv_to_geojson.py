import csv
import json
import h3

def csv_to_geojson(csv_file_path, geojson_file_path):
    features = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            latitude, longitude = h3.h3_to_geo(row['h3'])
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "properties": {
                    "temperature": float(row['lst'])
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file_path, 'w', encoding='utf-8') as geojsonfile:
        json.dump(geojson, geojsonfile, ensure_ascii=False, indent=4)

csv_to_geojson('lst_paris_2022.csv', 'LST_Paris_2022.geojson')