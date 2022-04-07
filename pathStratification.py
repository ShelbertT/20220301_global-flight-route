from greatCirclePath import *
from dataProcessing import *
from visualization import *


# Use Haversine formula to calculate great-circle distance in kilometers
def get_great_circle_distance(point1, point2):
    lon1 = point1[0]
    lat1 = point1[1]
    lon2 = point2[0]
    lat2 = point2[1]

    p = math.pi/180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a))  # 2*R*asin...


# Separate the single path into different levels
def break_path(path):
    index1 = 0
    index2 = 0
    for i in range(len(path)):
        forward = get_great_circle_distance(path[0], path[i])
        if forward > 300:
            index1 = i
            break
    for i in range(len(path)-1, -1, -1):
        backward = get_great_circle_distance(path[-1], path[i])
        if backward > 300:
            index2 = i
            break

    a = path[:(index1+1)]
    b = path[(index1+1):(index2-1)]
    c = path[index2:]

    return a, b, c


def generate_feature(properties, line, height_tag):
    origin_city = properties['origin'][1]
    destination_city = properties['destination'][1]
    result_properties = Properties(origin_city, destination_city, properties['count'], height_tag)

    feature_id = f'{origin_city}-{destination_city}-{height_tag}'
    result_feature = Feature(line, feature_id, result_properties.all)

    return result_feature


# Separate the path into different levels, indicating the different stages of flying
def path_stratification(all_paths):
    result = GeoJSON('path_cut')
    for feature in all_paths['features']:
        path = feature['geometry']['coordinates']
        properties = feature['properties']

        if get_great_circle_distance(path[0], path[-1]) < 600:
            continue
        else:
            a, b, c = break_path(path)

        print(get_great_circle_distance(c[0], c[-1]))

        feature_a = generate_feature(properties, a, 'A')
        feature_b = generate_feature(properties, b, 'B')
        feature_c = generate_feature(properties, c, 'C')

        result.add_feature(feature_a)
        result.add_feature(feature_b)
        result.add_feature(feature_c)

    # show_map(result.geojson)
    write_json(result.geojson, '4_stratification/stratified_path.geojson')

    return result.geojson


if __name__ == '__main__':
    flight_path = read_json('3_flight_path/flight_path.geojson')
    path_stratification(flight_path)

    # test = flight_path['features'][5]['geometry']['coordinates']
    # length = get_great_circle_distance(test[0], test[1])

# test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
