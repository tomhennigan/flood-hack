#
#  ___  ___ _ __ __ _ _ __   ___ _ __
# / __|/ __| '__/ _` | '_ \ / _ \ '__|
# \__ \ (__| | | (_| | |_) |  __/ |
# |___/\___|_|  \__,_| .__/ \___|_|
#                    |_|
#
# Methods for scraping volunteer data from FloodVolunteer.
#

import itertools
import leveldb
import requests
import re2 as re
from collections import namedtuple


# Define a bunch of regular expressions for parsing out data
_VOLUNTEER_MAP_LATLONG_PARSER = re.compile(r'latLng:\[([0-9.\-]+),([0-9.\-]+)\], data:.*?/offers/details/([0-9]+)')
_VOLUNTEER_LATLONG_PARSER = re.compile(r'latLng:\[([0-9.\-]+),([0-9.\-]+)\],')


# Define some structs
class Point(namedtuple('Point', ['lat', 'lng', 'volunteer_id'])):
    def __new__(cls, lat, lng, volunteer_id=None):
        return super(Point, cls).__new__(lat, lng, volunteer_id)


def scrape_volunteer_points(map_page_url, cache_db="/tmp/flood-volunteers.db"):
    """Scrape the map points from the FloodVolunteers home page. This method
    returns a generator of Volunteer objects."""

    r = requests.get(map_page_url)
    status = r.status_code
    if status != 200:
        raise Exception("Failed to load map page with status %r" % status)

    # Find the max volunteer
    max_volunteer_id = None
    for match in _VOLUNTEER_MAP_LATLONG_PARSER.finditer(r.text):
        lat, lng, volunteer_id = match.groups()
        max_volunteer_id = max(max_volunteer_id, int(volunteer_id))

    # Open the cache database if there is one
    cache = None
    last_volunteer = None
    if cache_db:
        cache = leveldb.LevelDB(cache_db)

        # Pull all the keys
        keys = cache.RangeIter(include_value=False)
        try:
            last_volunteer = keys.next()
        except Exception:
            pass
        else:
            last_volunteer = int(max(map(int, itertools.chain([last_volunteer], keys))))

    # Yield all the cached volunteers
    for key, value in cache.RangeIter(key_to=str(max_volunteer_id)):
        lat, lng, volunteer_id = value.split(",")
        yield Point(
            lat=float(lat),
            lng=float(lng),
            volunteer_id=volunteer_id
        )

    # Iterate over new volunteers and store them in the database
    start_volunteer = last_volunteer or 0
    for volunteer_id in xrange(start_volunteer + 1, max_volunteer_id + 1):
        url = "%s/maps/offer_map/%d" % (map_page_url.rstrip("/"), volunteer_id)
        r = requests.get(url)

        status = r.status_code
        if status != 200:
            continue

        match = _VOLUNTEER_LATLONG_PARSER.search(r.text)
        if match:
            lat, lng = match.groups()
            point = Point(
                lat=float(lat),
                lng=float(lng),
                volunteer_id=volunteer_id
            )

            if cache:
                cache.Put(str(volunteer_id), ",".join([str(lat), str(lng), str(volunteer_id)]))
            yield point
