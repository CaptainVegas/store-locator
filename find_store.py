"""
find_store

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>          Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address            Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)      Display units in miles or kilometers [default: mi]
  --output=(text|json) Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
"""

from collections import OrderedDict
from math import sin, cos, sqrt, asin, atan2, radians

import sys
import csv
import argparse
import requests

# Constants
GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
KILOMETERS_TO_MILES = 0.621371
RADIUS_OF_THE_EARTH_KILOMETERS = 6373.0

def load_store_location_data():
    """Load the store location data from the csv file included in the project"""
    try:
        store_location_data = []
        with open('store-locations.csv') as csvfile:
            reader = csv.DictReader(csvfile, dialect=csv.excel)
            for row in reader:
                store_location_data.append(dict(OrderedDict(row)))

        return store_location_data
    except IOError as error:
        print("I/O error({0}): {1}".format(error.errno, error.strerror))
        return None

def get_location_data(address=None):
    """Call Google Maps Geocoding API to determine the Longitude and Latitude of this address/zipcode"""
    params = {
        'address': address,
        'sensor': 'false'
    }

    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    # Use the first result
    result = res['results'][0]

    try:
        geodata = dict()
        geodata['Latitude'] = result['geometry']['location']['lat']
        geodata['Longitude'] = result['geometry']['location']['lng']
        return geodata
    except Exception:
        return None

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def find_closest_store(data, v):
    return min(data, key=lambda p: distance(float(v['Latitude']), float(v['Longitude']), float(p['Latitude']), float(p['Longitude'])))

def find_distance_to_store(latitude1, longitude1, latitude2, longitude2):
    """Find the distance between the store and the provided address based on the Latitude and Longitude"""
    lat1 = float(latitude1)
    lon1 = float(longitude1)
    lat2 = float(latitude2)
    lon2 = float(longitude2)

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance_in_kilometers = RADIUS_OF_THE_EARTH_KILOMETERS * c

    return distance_in_kilometers

def convert_km_to_miles(kilometers):
    miles = kilometers * KILOMETERS_TO_MILES
    return miles

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(description='Find Store: find_store will locate the nearest store (as the crow flies) from store-locations.csv, print the matching store address, as well as the distance to that store.')
    parser.add_argument('-a', '--address', dest='address', help='Customer address', default=None)
    parser.add_argument('-z', '--zip', dest='zip', help='Customer zipcode', default=None)
    parser.add_argument('-u', '--units', dest='units', help='Units (mi|km)', default=None)
    parser.add_argument('-o', '--output', dest='output', help='Output (text|json)', default=None)
    args = parser.parse_args(argv)

    user_location = None
    if args.address is not None:
        user_location = args.address

    if args.zip is not None:
        user_location = args.zip

    if user_location is not None:
        # Load the store location data from a file
        store_location_data = load_store_location_data()

        # Lookup Location data for this address/zipcode
        customer_location = get_location_data(user_location)

        if customer_location is not None:
            # Find the closet store based on the latitude/longitude
            query_coordinates = {'Latitude': customer_location["Latitude"], 'Longitude': customer_location["Longitude"]}
            closet_store = find_closest_store(store_location_data, query_coordinates)

            if closet_store is not None:
                distance_to_store = None
                # Find the distance to this store
                kilometers_to_store = find_distance_to_store(customer_location["Latitude"], customer_location["Longitude"], closet_store['Latitude'], closet_store['Longitude'])
                # Convert to miles
                miles_to_store = convert_km_to_miles(kilometers_to_store)
                distance_to_store = "{0:.2f} mi".format(miles_to_store)

                # Check if we need to return the distance in kilometers
                if args.units is not None:
                    if args.units == 'km':
                        distance_to_store = "{0:.2f} km".format(kilometers_to_store)

                # Add the distance to the store to our store data
                if distance_to_store is not None:
                    closet_store['Distance to Store'] = distance_to_store

                # Check if we need to change the format of the output
                format_as_text = False
                if args.output is not None:
                    if args.output == 'text':
                        format_as_text = True

                # Print the results
                if format_as_text:
                    print("Store Name: ", closet_store['Store Name'])
                    print("Store Location: ", closet_store['Store Location'])
                    print("Address: ", closet_store['Address'])
                    print("City: ", closet_store['City'])
                    print("State: ", closet_store['State'])
                    print("Zip Code: ", closet_store['Zip Code'])
                    if distance_to_store is not None:
                        print("Distance to Store: ", closet_store['Distance to Store'])
                else:
                    print(closet_store)
    else:
        parser.print_help()

if __name__ == "__main__":
    sys.exit(main())
