from unittest import TestCase

from glineenc import encode_pairs
from glineenc.encode import encode_lat_or_long


class TestGLineEnc(TestCase):
    def test_encode_negative(self):
        f = -179.9832104
        self.assertEqual(encode_lat_or_long(f, 0)[0], "`~oia@")

        f = -120.2
        self.assertEqual(encode_lat_or_long(f, 0)[0], "~ps|U")

    def test_encode_positive(self):
        f = 38.5
        self.assertEqual(encode_lat_or_long(f, 0)[0], "_p~iF")

    def test_encode_one_pair(self):
        pairs = [(38.5, -120.2)]
        expected_encoding = "_p~iF~ps|U", "B"
        self.assertEqual(encode_pairs(pairs), expected_encoding)

    def test_encode_pairs(self):
        pairs = (
            (38.5, -120.2),
            (40.7, -120.95),
            (43.252, -126.453),
            (40.7, -120.95),
        )
        expected_encoding = "_p~iF~ps|U_ulLnnqC_mqNvxq`@~lqNwxq`@", "BBBB"
        self.assertEqual(encode_pairs(pairs), expected_encoding)

        pairs = (
            (37.4419, -122.1419),
            (37.4519, -122.1519),
            (37.4619, -122.1819),
        )
        expected_encoding = "yzocFzynhVq}@n}@o}@nzD", "B@B"
        self.assertEqual(encode_pairs(pairs), expected_encoding)
