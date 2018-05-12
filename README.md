# Requirements

The application is build with python3.6, but it should work all python 3 version

- docopt==0.6.2
- pandas==0.22.0
- requests==2.18.4
- urllib3==1.22

# Details

Command-line application that find closes store for specified address

```
Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

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
```

# How to use

First install all dependancies.

```
pip install -r requirements.txt
```

Possible usage of the application

```
Examples:
   ./find_store --address="1770 Union St, San Francisco, CA 94123"
   ./find_store --zip=94115 --units=km    
   ./find_store --zip=94115 --output=json
```

# About project

```
.
├── find_store -> find_store.py     - symlink to main app
├── find_store.py                   - main app
├── README.md                       - this readme file
├── requirements.txt                - dependacies for the project
├── store-locations.csv             - data file
└── tests.py                        - unit tests
```

Application does two things:
1. Find coordinates based on address or zipcode.
2. Calculate distance for each store, sort and select closest store

Google Geocode API is used to get coordinates.
Set `API_KEY` into env to avoid problems with quota API limit. (optional)

Pandas library is used to manipulate data from csv file.
Distance is calculated with Haversine formula.

Tests (unit tests) are located in tests.py, that basically check:
- function find_coordinate
- existence of csv file
- app external call

