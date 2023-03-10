from typing import Tuple

from .types import Points
from .util import (
    NUM_LEVELS,
    douglas_peucker_distances,
    encode_signed,
    encode_unsigned,
    get_level_for_distance_from_line,
)


def encode_pairs(points: Points) -> Tuple[str, str]:
    """Encode a sequence of latitude/longitude pairs.

    Args
        points:
            A sequence of latitude/longitude pairs.

            NOTE: Ordering is *latitude* first.

    Returns
        A tuple with the following items:
            - An encoded string representing points within the error
              threshold
            - An encoded string representing the maximum zoom level for
              each of those points

    Example::

        >>> pairs = ((38.5, -120.2), (43.252, -126.453), (40.7, -120.95))
        >>> encode_pairs(pairs)
        ('_p~iF~ps|U_c_\\\\fhde@~lqNwxq`@', 'BBB')

    """
    encoded_points = []
    encoded_levels = []

    distances = douglas_peucker_distances(points)
    points_of_interest = []
    for i, distance in enumerate(distances):
        if distance is not None:
            lat, long = points[i]
            points_of_interest.append((lat, long, distance))

    lat_prev, long_prev = 0, 0
    for lat, long, dist in points_of_interest:
        encoded_lat, lat_prev = encode_lat_or_long(lat, lat_prev)
        encoded_long, long_prev = encode_lat_or_long(long, long_prev)
        encoded_level = encode_level_for_distance(dist)

        encoded_points.append(encoded_lat)
        encoded_points.append(encoded_long)
        encoded_levels.append(encoded_level)

    encoded_points_str = "".join(encoded_points)
    encoded_levels_str = "".join(encoded_levels)
    return encoded_points_str, encoded_levels_str


def encode_lat_or_long(x: float, prev: int) -> Tuple[str, int]:
    """Encode a single latitude or longitude.

    Args:
        x:
            The latitude or longitude to encode.

        prev:
            The int value of the previous latitude or longitude; used
            to calculate a delta, which is the value that is actually
            encoded.

    Example::

        >>> encoded_x, x_prev = encode_lat_or_long(-179.9832104, 0)
        >>> encoded_x
        '`~oia@'
        >>> x_prev
        -17998321
        >>> encode_lat_or_long(-120.2, x_prev)
        ('al{kJ', -12020000)

    """
    int_value = int(x * 1e5)
    delta = int_value - prev
    return encode_signed(delta), int_value


def encode_level_for_distance(distance) -> str:
    level = get_level_for_distance_from_line(distance)
    return encode_unsigned(NUM_LEVELS - level - 1)
