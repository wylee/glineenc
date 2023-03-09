# GLineEnc

GLineEnc is a Google Maps Polyline Encoder--it encodes line geometries
such that they can be rendered more efficiently in the browser.

The encoding algorithm is described [here](https://developers.google.com/maps/documentation/utilities/polylinealgorithm).

## Usage

GLineEnc exposes a single API function, `encode_pairs`. This function
accepts a sequence of latitude/longitude pairs and returns a string
representing the encoded points and another string indicating the
maximum zoom level at which each point should be displayed:

```python
>>> from glineenc import encode_pairs
>>> result = encode_pairs([(38.5, -120.2), (43.252, -126.453)])
>>> result
('_p~iF~ps|U_c_\\fhde@', 'BB')
```

You could JSONify the result like this to pass it to the browser:

```python
>>> import json
>>> json.dumps({'points': result[0], 'levels': result[1]})
'{"points": "_p~iF~ps|U_c_\\\\fhde@", "levels": "BB"}'
```

On the client, you would create a line from this encoded data like so:

```javascript
new google.maps.Polyline({
  path: google.maps.geometry.encoding.decodePath(path)
});
```

[Reference](https://developers.google.com/maps/documentation/javascript/examples/geometry-encodings)
