#
#
#

from scraper import scrape_volunteer_points, Point
from util import points_within_distance


def get_volunteers():
    """Return a generator of scraper.Volunteer objects describing volunteers."""

    return scrape_volunteer_points("http://floodvolunteers.co.uk/")
