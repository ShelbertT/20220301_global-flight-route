import time
import requests
import os
import sys
import getpass
import json

base_address = "http://localhost:8000/"
camera = "arcgisearth/camera"
snapshot = "arcgisearth/snapshot"
addgraphic = "arcgisearth/graphics"


def get_camera():
    url = base_address + camera
    r = requests.get(url, verify=False)
    print(r.content)
    return r.content


def draw_point(point, id):
    location = f'''
        {{
            "id": "{id}",
            "geometry": {{
                "type": "point",
                "x": {point[0]},
                "y": {point[1]}
            }},
            "symbol": {{
                "type": "picture-marker",
                "url": "https://static.arcgis.com/images/Symbols/Shapes/BlackStarLargeB.png",
                "width": "20px",
                "height": "20px",
                "angle":0,
                "xoffset": "0px",
                "yoffset": "0px"
            }}
        }}
        '''
    url = base_address + addgraphic
    headers = {'content-Type': 'application/json'}
    r = requests.post(url, data=location, headers=headers, verify=False)


def draw_line():
    location = f'''
    {{
      "id": "polyline-simple-line-graphic",
      "geometry": {{
             "type": "polyline",
             "paths": [
                 [
                    -118,
                    34
                  ],
                 [
                    -100,
                    40
                  ],
                 [
                    -82,
                    34
                  ]
              ]
           }},
            "symbol": {{
               "type": "simple-line",
               "color": "#33cc33",
               "width": "2px"
            }}
     }}'''

    url = base_address + addgraphic
    headers = {'content-Type': 'application/json'}
    r = requests.post(url, data=location, headers=headers, verify=False)


if __name__ == '__main__':
    draw_point((0, 0), 1)
    draw_line()

