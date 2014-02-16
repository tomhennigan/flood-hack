#
#  ___  ___ _ __ __ _ _ __   ___ _ __
# / __|/ __| '__/ _` | '_ \ / _ \ '__|
# \__ \ (__| | | (_| | |_) |  __/ |
# |___/\___|_|  \__,_| .__/ \___|_|
#                    |_|
#
# Methods for scraping volunteer data from FloodVolunteer.
#

import requests
import re2 as re
from collections import namedtuple


# Define a bunch of regular expressions for parsing out data
_VOLUNTEER_LATLONG_PARSER = re.compile(r'latLng:\[([0-9.\-]+),([0-9.\-]+)\]')

# Define some structs
Point = namedtuple('Point', ['lat', 'lng'])


def scrape_volunteer_points(map_page_url):
    """Scrape the map points from the FloodVolunteers home page. This method
    returns a generator of Volunteer objects."""

    r = requests.get(map_page_url)
    status = r.status_code
    if status != 200:
        raise Exception("Failed to load map page with status %r" % status)

    for match in _VOLUNTEER_LATLONG_PARSER.finditer(r.text):
        lat, lng = match.groups()

        yield Point(lat=float(lat), lng=float(lng))
