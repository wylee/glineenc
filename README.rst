GLineEnc
++++++++

GLineEnc is a Google Maps Polyline Encoder--it encodes line geometries
such that they can be rendered more efficiently in the browser.

The encoding algorithm is described here::

    https://developers.google.com/maps/documentation/utilities/polylinealgorithm

Installation
============

GLineEnc is packaged as a standard distutils distribution. It can be
installed via easy_install, pip, `python setup.py install`, or by adding
it to the `install_requires` list in your setup.py. For example::

    pip install glineenc

Usage
=====

GLineEnc exposes a single API function, `encode_pairs`. This function
accepts a sequence of latitude/longitude pairs and returns a string
representing the encoded points and another string indicating the
maximum zoom level at which each point should be displayed::

    >>> from glineenc import encode_pairs
    >>> result = encode_pairs([(38.5, -120.2), (43.252, -126.453)])
    >>> result
    ('_p~iF~ps|U_c_\\fhde@', 'BB')

You could JSONify the result like this to pass it to the browser::

    >>> import json
    >>> json.dumps({'points': result[0], 'levels': result[1]})
    '{"points": "_p~iF~ps|U_c_\\\\fhde@", "levels": "BB"}'

On the client, you would create a line from this encoded data like so::

    // It's assumed here that you've decoded the JSON object created
    // above into a local var named `result`.
    var path = google.maps.geometry.encoding.decodePath(result.points);
    var myLine = new google.maps.Polyline({path: path});

In Google Maps v2, that would look like this instead::

    var myLine = new GPolyline.fromEncoded({
        points: result.points,
        levels: result.levels
    });
