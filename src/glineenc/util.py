from math import sqrt
from typing import List, Optional

from .types import Line, Point, Points


# TODO: Ideally, these wouldn't be hard coded.
THRESHOLD = 0.00001
NUM_LEVELS = 4
ZOOM_FACTOR = 32

ZOOM_LEVEL_BREAKS = [
    THRESHOLD * (ZOOM_FACTOR ** (NUM_LEVELS - i - 1)) for i in range(NUM_LEVELS)
]


def douglas_peucker_distances(points: Points) -> List[Optional[float]]:
    num_points = len(points)

    distances: List[Optional[float]] = [None] * num_points
    distances[0] = THRESHOLD * (ZOOM_FACTOR**NUM_LEVELS)
    distances[-1] = distances[0]

    if num_points < 3:
        return distances

    stack = [(0, num_points - 1)]
    while stack:
        a, b = stack.pop()
        max_dist = 0.0
        for i in range(a + 1, b):
            dist = distance_from_line(points[i], (points[a], points[b]))
            if dist > max_dist:
                max_dist = dist
                max_i = i
        if max_dist > THRESHOLD:
            distances[max_i] = max_dist
            stack.append((a, max_i))
            stack.append((max_i, b))

    return distances


def distance_from_line(point: Point, line: Line) -> float:
    """Compute distance of `point` from `line`."""
    x, y = point
    a, b = line

    if a == b:
        return sqrt((b[0] - x) ** 2 + (b[1] - y) ** 2)

    u = (((x - a[0]) * (b[0] - a[0])) + ((y - a[1]) * (b[1] - a[1]))) / (
        ((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2)
    )

    if u <= 0:
        result = sqrt(((x - a[0]) ** 2) + ((y - a[1]) ** 2))
    elif u >= 1:
        result = sqrt(((x - b[0]) ** 2) + ((y - b[1]) ** 2))
    else:
        result = sqrt(
            (((x - a[0]) - (u * (b[0] - a[0]))) ** 2)
            + (((y - a[1]) - (u * (b[1] - a[1]))) ** 2)
        )

    return result


def get_level_for_distance_from_line(distance: float) -> int:
    if distance < THRESHOLD:
        return 0
    level = 0
    while distance < ZOOM_LEVEL_BREAKS[level]:
        level += 1
    return level


def encode_signed(n: int) -> str:
    tmp = n << 1
    if n < 0:
        tmp = ~tmp
    return encode_unsigned(tmp)


def encode_unsigned(n: int) -> str:
    tmp = []
    while n >= 0b100000:
        tmp.append(n & 0b11111)
        n >>= 5
    tmp = [(c | 0b100000) for c in tmp] + [n]
    chars = [chr(i + 0b111111) for i in tmp]
    result = "".join(chars)
    return result
