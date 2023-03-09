import math
from typing import List, Sequence, Tuple


Point = Tuple[float, float]
Points = Sequence[Point]


threshold = 0.00001
num_levels = 4
zoom_factor = 32
zoom_level_breaks = [
    threshold * (zoom_factor ** (num_levels - i - 1)) for i in range(num_levels)
]


def encode_pairs(points: Points) -> Tuple[str, str]:
    """Encode a sequence of latitude/longitude pairs.

    Args
        points: A sequence of latitude/longitude pairs.

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
    for i, d in enumerate(distances):
        if d is not None:
            lat, long = points[i]
            points_of_interest.append((lat, long, d))

    lat_prev, long_prev = 0, 0
    for lat, long, d in points_of_interest:
        encoded_lat, lat_prev = encode_lat_or_long(lat, lat_prev)
        encoded_long, long_prev = encode_lat_or_long(long, long_prev)
        encoded_points.append(encoded_lat)
        encoded_points.append(encoded_long)
        encoded_level = encode_unsigned(num_levels - compute_level(d) - 1)
        encoded_levels.append(encoded_level)

    encoded_points_str = "".join(encoded_points)
    encoded_levels_str = "".join(encoded_levels)
    return encoded_points_str, encoded_levels_str


def encode_lat_or_long(x: float, prev: int) -> Tuple[str, int]:
    """Encode a single latitude or longitude.

    Args:
        x: The latitude or longitude to encode
        prev: The int value of the previous latitude or longitude

    Example::

        >>> x = -179.9832104
        >>> encoded_x, prev = encode_lat_or_long(x, 0)
        >>> encoded_x
        '`~oia@'
        >>> prev
        -17998321
        >>> x = -120.2
        >>> encode_lat_or_long(x, prev)
        ('al{kJ', -12020000)

    """
    int_value = int(x * 1e5)
    delta = int_value - prev
    return encode_signed(delta), int_value


def encode_signed(n: int) -> str:
    tmp = n << 1
    if n < 0:
        tmp = ~tmp
    return encode_unsigned(tmp)


def encode_unsigned(n: int) -> str:
    tmp = []
    while n >= 0b100000:
        tmp.append(n & 0b11111)
        n = n >> 5
    tmp = [(c | 0b100000) for c in tmp] + [n]
    tmp = [chr(i + 0b111111) for i in tmp]
    tmp = "".join(tmp)
    return tmp


def douglas_peucker_distances(points: Points) -> List[float]:
    distances = [None] * len(points)
    distances[0] = threshold * (zoom_factor ** num_levels)
    distances[-1] = distances[0]

    if len(points) < 3:
        return distances

    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        max_dist = 0.0
        for i in range(a + 1, b):
            dist = distance(points[i], points[a], points[b])
            if dist > max_dist:
                max_dist = dist
                max_i = i
        if max_dist > threshold:
            distances[max_i] = max_dist
            stack.append((a, max_i))
            stack.append((max_i, b))

    return distances


def distance(point: Point, a, b) -> float:
    """Compute distance of `point` from line `a` `b`."""
    if a == b:
        return math.sqrt((b[0] - point[0]) ** 2 + (b[1] - point[1]) ** 2)

    u = (
        ((point[0] - a[0]) * (b[0] - a[0])) + ((point[1] - a[1]) * (b[1] - a[1]))
    ) / (((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2))

    if u <= 0:
        result = math.sqrt(((point[0] - a[0]) ** 2) + ((point[1] - a[1]) ** 2))
    elif u >= 1:
        result = math.sqrt(((point[0] - b[0]) ** 2) + ((point[1] - b[1]) ** 2))
    elif 0 < u < 1:
        result = math.sqrt(
            ((((point[0] - a[0]) - (u * (b[0] - a[0]))) ** 2))
            + ((((point[1] - a[1]) - (u * (b[1] - a[1]))) ** 2))
        )

    return result


def compute_level(distance: float) -> int:
    # XXX: If the distance happens to be very small, this will fail
    #      with an `UnboundLocalError`.
    if distance > threshold:
        level = 0
    while distance < zoom_level_breaks[level]:
        level += 1
    return level
