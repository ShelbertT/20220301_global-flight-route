# from greatCirclePath import *
# from dataProcessing import *
# from visualization import *
from generateFlightPath import *
from pathStratification import *


def main():
    # data = read_json('data/flights2.json')
    # extract_od(data)  # This step will also write a copy of od

    all_od = read_json('2_cache/all_od.json')
    generate_flight_path(all_od)  # This step will also write a copy of generated flight_path
    flight_path = read_json('3_flight_path/flight_path.geojson')
    path_stratification(flight_path)


if __name__ == '__main__':
    main()
