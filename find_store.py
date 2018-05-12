#!/usr/bin/env python
"""
Usage:
  find_store --address=<address>
  find_store --address=<address> [--units=(mi|km)] [--output=(text|json)]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=(text|json)]

Options:
  --zip=<zip>           Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>   Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)       Display units in miles or kilometers [default: mi]
  --output=(text|json)  Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]
"""

# Example
#   ./find_store --address="1770 Union St, San Francisco, CA 94123"
#   ./find_store --zip=94115 --units=km    
#   ./find_store --zip=94115 --output=json

from docopt import docopt
import pandas as pd
import requests
import urllib.parse
from math import radians, cos, sin, asin, sqrt
import os

API_KEY = os.environ.get('API_KEY')

def find_coordinate(address):
    """
    :type address: str - Address or zipcode ('1770 Union St, San Francisco, CA 94123' or '95125')
    :rtype: dict - format: {'lat':float, 'lng':float}
    """
    if not address:
      raise ValueError('address is emprty')

    key = '&key=' + API_KEY if API_KEY else ''

    address = urllib.parse.quote_plus(address, safe=',')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + key
    response = requests.get(url)
    resp = response.json()
    if resp['results']:
      loc = resp['results'][0]['geometry']['location']
    else:
      raise ValueError(resp['error_message'])

    return loc


# Used from here https://www.geeksforgeeks.org/program-distance-two-points-earth/
def haversine(lat1, lon1, lat2, lon2, unit='mi'):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth - 6371 in kilometers, 3956 in miles
    r = 6371
    km = 6371 * c
    mi = 3956 * c
    
    return km if unit == 'km' else mi


def main(args):
    address = args.get('--address') or args.get('--zip')
    units = args.get('--units')
    output = args.get('--output')

    # get coordinate
    loc = find_coordinate(address)
    # load data with panda
    oo = pd.read_csv('./store-locations.csv')
    # calculate Dist field
    oo['Dist'] = oo.apply(lambda row:  haversine(row['Latitude'],row['Longitude'], loc['lat'], loc['lng'], units), axis=1)
    # sort by Dist
    df = oo.sort_values('Dist')
    # get first store - therefore the closest one
    first = df.head(1)[['Store Location', 'Dist']].iloc[0]

    if output == 'json':
        print({
          'Location': first['Store Location'], 
          'Dist': "{0:.2f} {1}".format(first['Dist'], units)
        })
    else:
        print("{0}, {1:.2f} {2}".format(first['Store Location'], first['Dist'], units))


if __name__== "__main__":
    args = docopt(__doc__, version='1.0')
    main(args)