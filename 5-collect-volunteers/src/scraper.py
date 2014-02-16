#
#  ___  ___ _ __ __ _ _ __   ___ _ __
# / __|/ __| '__/ _` | '_ \ / _ \ '__|
# \__ \ (__| | | (_| | |_) |  __/ |
# |___/\___|_|  \__,_| .__/ \___|_|
#                    |_|
#
#  CLI tool for scraping FloodVolunteers.co.uk and extracing their details
#

import requests


def scrape_volunteer_points(map_page_url):
    """Scrape the map points from the FloodVolunteers home page."""

    r = requests.get(map_page_url)
    status = r.status_code
    if status != 200:
        raise Exception("Failed to load map page with status %r" % status)
