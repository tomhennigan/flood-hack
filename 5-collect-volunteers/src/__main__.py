#
#            _ _           _                  _             _
#   ___ ___ | | | ___  ___| |_    __   _____ | |_   _ _ __ | |_ ___  ___ _ __ ___
#  / __/ _ \| | |/ _ \/ __| __|___\ \ / / _ \| | | | | '_ \| __/ _ \/ _ \ '__/ __|
# | (_| (_) | | |  __/ (__| ||_____\ V / (_) | | |_| | | | | ||  __/  __/ |  \__ \
#  \___\___/|_|_|\___|\___|\__|     \_/ \___/|_|\__,_|_| |_|\__\___|\___|_|  |___/
#
#  CLI tool for scraping FloodVolunteers.co.uk and extracing their details
#

import argparse
from pprint import pprint

from scraper import scrape_volunteer_points


def main(args):
    """Things happen here."""

    url = "http://floodvolunteers.co.uk/"
    points = scrape_volunteer_points(map_page_url=url)
    pprint(points)


def parse_args():
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(prog="volunteers")
    return parser.parse_args()


if __name__ == "__main__":
    exit(main(parse_args()))
