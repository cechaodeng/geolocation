#!/usr/bin/env python2.7

import json
import requests

location_list_json = "location.json"
location_list_txt = "location.txt"

output_lat_lng = "output_lat_lng.txt"
output_error_log = "output_error_log.log"

# read name from json
# with open(hotel_list_json, 'r') as f:
#     location_list_geo_data = json.load(f)

# read name from txt
with open(location_list_txt, 'r') as f:
    location_list_geo_data = f.readlines()

for location_geo_line in location_list_geo_data:
    # from txt
    location_geo_arr = location_geo_line.strip('\n').split(" : ")
    location_geo_str = "{\"id\" : " + location_geo_arr[0] + ",\"name\" : \"" + location_geo_arr[1] + "\"}"
    location_geo = json.loads(location_geo_str)

    geo_search_prefix = "https://api.opencagedata.com/geocode/v1/json?q="
    # Your Opencagedata App Key
    opencagedata_key = "Your Opencagedata App Key"
    geo_search_key = "&key=" + opencagedata_key
    geo_search_annotation = "&no_annotations=1"
    geo_search_language = "&language=en"

    geo_search_endpoint = geo_search_prefix + location_geo["name"] + geo_search_key + geo_search_annotation + geo_search_language
    resp = requests.get(geo_search_endpoint)
    # print geo_search_endpoint
    # print resp.status_code
    if (resp.status_code == 200):
        try:
            resp_geo_location_json = resp.json()["results"][0]["geometry"]
            lat = resp_geo_location_json['lat']
            lng = resp_geo_location_json['lng']
        except IndexError as e:
            # google api
            geo_search_prefix_goole =  "https://maps.googleapis.com/maps/api/geocode/json?address="
            # Your Google App Key
            google_key = "Your Google App Key"
            geo_search_key_google = "&key=" + google_key

            # get geometry from google api
            geo_search_endpoint = geo_search_prefix_goole + location_geo["name"] + geo_search_key_google
            resp = requests.get(geo_search_endpoint)
            if (resp.status_code == 200):
                try:
                    resp_geo_location_json = resp.json()["results"][0]["geometry"]["location"]
                    lat = resp_geo_location_json['lat']
                    lng = resp_geo_location_json['lng']
                except IndexError as e:
                    location_cannot_parse = str(location_geo["id"]) + ' : ' + (location_geo['name']).encode('utf-8') + ' : ' + str(e) + ';\n'

                    # write error log
                    with open(output_error_log, 'a+') as f_cannot_parse:
                        f_cannot_parse.write(location_cannot_parse)
                    continue
            else:
                print(resp.status_code + "::" + resp.reason)

        target_str = str(location_geo["id"]) + " : " + str(location_geo["name"]) + " : " + str(lat) + " : " + str(lng)

        with open(output_lat_lng, 'a+') as f_target:
            f_target.write(target_str)
    else:
        with open(output_error_log, 'a+') as f_cannot_parse:
            f_cannot_parse.write(location_cannot_parse)

