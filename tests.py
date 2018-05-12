#!/usr/bin/env python
import unittest
from find_store import find_coordinate
import json
import os.path
from time import sleep
import subprocess

class TestFindStore(unittest.TestCase):

    def test_find_coordinate(self):
        try:
            loc1 = find_coordinate('1770 Union St, San Francisco, CA 94123')
            loc2 = {'lat': 37.7981539, 'lng': -122.4284318}
            self.assertEqual(json.dumps(loc1),  json.dumps(loc2))
        except ValueError as err:
            self.assertEqual(str(err).split('.')[0],  'You have exceeded your daily request quota for this API')

    def test_find_coordinate_noinput(self):
        # check that find_coordinate fails with no input
        with self.assertRaises(TypeError):
            find_coordinate()     

        with self.assertRaises(ValueError):
            find_coordinate('')     

    def test_locate_file(self):
        self.assertTrue(os.path.isfile('./store-locations.csv') )

    def test_find_program(self):        
        # find_store.py --zip=94115 --output=json
        out = subprocess.check_output(['./find_store','--zip=94115', '--output=json'])       
        self.assertEqual(out, b"{'Location': 'SEC Geary Blvd. and Masonic Avenue', 'Dist': '0.60 mi'}\n")
        

if __name__ == '__main__':
    unittest.main()