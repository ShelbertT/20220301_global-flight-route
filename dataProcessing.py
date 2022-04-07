import json


# Creating Geojson-------------------------------------------------------------------------------------------------------
class GeoJSON:  # Access through self.geojson
    def __init__(self, name):
        self.name = name

        self.geojson = {
            "name": name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": [],
            "type": "FeatureCollection"
        }

    def add_feature(self, feature):  # Feature class
        self.geojson["features"].append(feature.feature)


class Feature:  # Access through self.feature
    def __init__(self, line, feature_id, properties={}):
        self.feature_id = feature_id

        self.feature = {
            "geometry": {
                "coordinates": line,
                "type": "LineString"
            },
            "id": feature_id,
            "properties": properties,
            "type": "Feature"
        }

    def add_line(self, line):  # list[list[x, y]]
        self.feature["geometry"]["coordinates"] += line

    def add_property(self, property):  # dict{}
        self.feature["geometry"]["properties"].update(property)


class Properties:  # Access through self.all
    def __init__(self, origin, destination, count, height=0):
        self.all = {
            "origin": origin,
            "destination": destination,
            "count": count,
            "height": height
        }


# JSON------------------------------------------------------------------------------------------------------------------
def read_json(input_path):  # path -> dict | 输入文件路径，返回存储该json的字典
    with open(input_path, encoding='utf-8') as f:
        resp = json.load(f)
        return resp


def write_json(data, output_path='test.json', indent=True):  # dict -> json | 把字典写入本地json文件
    with open(output_path, "w", encoding='utf-8') as f:
        # json.dump(dict_var, f)  # 写为一行
        if indent:
            json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
        else:
            json.dump(data, f, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    data = read_json('1_data/flights2.json')
    write_json(data)