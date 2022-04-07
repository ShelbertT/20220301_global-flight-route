from greatCirclePath import *
from dataProcessing import *
from visualization import *

# geojson to kml: https://anyconv.com/geojson-to-kml-converter/


def generate_flight_path(all_od, name='flight_path.geojson'):  # o-d collection -> GeoJSON | generate flight path based on od, and write it into local disk
    flight_path = GeoJSON("flight_path")

    current = 0
    for od in all_od:
        flight_path.add_feature(generate_paths_feature(od))
        current += 1
        print(f'{current}/{len(all_od)}')

    write_json(flight_path.geojson, f'3_flight_path/{name}')
    print('Finished writing flight path')

    return flight_path


def generate_paths_feature(od):  # o-d point -> Feature class | generate a single path
    origin = od['origin']
    destination = od['destination']

    # generate all it takes to initialize a Feature class
    line = create_path(origin[3], origin[4], destination[3], destination[4])
    feature_id = f'{origin[1]}-{destination[1]}'
    prop = Properties(origin=origin[:3], destination=destination[:3], count=od['count'])

    path = Feature(line=line, feature_id=feature_id, properties=prop.all)

    return path


def delete_none(all_od):  # json | delete all OD that's missing at least one coord
    for i in range(len(all_od)-1, -1, -1):  # traverse from last, since we will be deleting items from it.
        lon1 = all_od[i]["origin"][3]
        lat1 = all_od[i]["origin"][4]
        lon2 = all_od[i]["destination"][3]
        lat2 = all_od[i]["destination"][4]
        if lon1 is None or lat1 is None or lon2 is None or lat2 is None:
            all_od.remove(all_od[i])


def extract_od(raw_data):  # json -> dict | extract all o-d from original data. A-B & B-A are seen as the same, only extract the count. NOTE: this function modifies the origin input
    # sort and extract routes
    all_routes = []
    for route in raw_data['routes']:
        if route[1] < route[2]:
            route_reorder = (route[0], route[1], route[2])
        else:
            route_reorder = (route[0], route[2], route[1])
        all_routes.append(route_reorder)
    routes = set(all_routes)

    all_od = []
    current = 0
    num = len(routes)

    for route in routes:
        info = {
            "origin": raw_data['airports'][route[1]],
            "destination": raw_data['airports'][route[2]],
            "count": all_routes.count(route)
        }
        all_od.append(info)
        current += 1
        print(f'{current}/{num}')

    delete_none(all_od)
    write_json(all_od, '2_cache/all_od.json')


if __name__ == '__main__':
    main()

