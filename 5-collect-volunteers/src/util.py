#
#        _   _ _
#  _   _| |_(_) |
# | | | | __| | |
# | |_| | |_| | |
#  \__,_|\__|_|_|
#
#
#

from math import sin, cos, sqrt, atan2, radians


def points_within_distance(center, points, radius=1):
    """Returns all points from points that are within radius from the center.

    :param center: the center Point obejct.
    :param points: iterable of Point objects to filter.
    :param radius: a float value for the radius (in meters).
    :returns: a generator of points
    """

    radius_km = radius / 1000

    center_lat = radians(center.lat)
    center_lng = radians(center.lng)

    # Calculate which points are within the radius
    for point in points:
        point_lat = radians(point.lat)
        point_lng = radians(point.lng)

        distance_lat = point_lat - center_lat
        distance_lng = point_lng - center_lng

        a = (sin(distance_lat / 2)) ** 2 + cos(center_lat) * cos(point_lat) * (sin(distance_lng / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6378.1 * c

        if distance <= radius_km:
            yield point
