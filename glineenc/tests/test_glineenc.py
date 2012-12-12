#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from glineenc import encode_lat_or_long, encode_pairs


def test_encode_negative():
    f = -179.9832104
    assert encode_lat_or_long(f, 0)[0] == '`~oia@'

    f = -120.2
    assert encode_lat_or_long(f, 0)[0] == '~ps|U'


def test_encode_positive():
    f = 38.5
    assert encode_lat_or_long(f, 0)[0] == '_p~iF'


def test_encode_one_pair():
    pairs = [(38.5, -120.2)]
    expected_encoding = '_p~iF~ps|U', 'B'
    assert encode_pairs(pairs) == expected_encoding


def test_encode_pairs():
    pairs = (
        (38.5, -120.2),
        (40.7, -120.95),
        (43.252, -126.453),
        (40.7, -120.95),
    )
    expected_encoding = '_p~iF~ps|U_ulLnnqC_mqNvxq`@~lqNwxq`@', 'BBBB'
    assert encode_pairs(pairs) == expected_encoding

    pairs = (
        (37.4419, -122.1419),
        (37.4519, -122.1519),
        (37.4619, -122.1819),
    )
    expected_encoding = 'yzocFzynhVq}@n}@o}@nzD', 'B@B'
    assert encode_pairs(pairs) == expected_encoding
