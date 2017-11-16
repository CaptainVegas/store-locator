## Store Locator

Store locator is a command-line application that takes an address or zip code as an input and then locates the nearest store.  

The list of store locations data comes from a file included within the project and uses the Google Maps Geocoding API to determine the Longitude and Latitude of the entered address. Distance between the store and the address entered by the user is calculated using the Haversine formula.  

## Usage

```
Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>          Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address            Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)      Display units in miles or kilometers [default: mi]
  --output=(text|json) Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
```

## Setup

This applications relies on the request module.

```
pip install requests
```

## Testing

Tests of the functions of this application are implement with python's unitest and can be run with the following command.

```
python test_find_store.py
```
## Limitions
  The Google Maps Geocoding API has a limit on the number of free request made to this service and key would be required for production use.

## References

  Google Maps Geocoding API: https://developers.google.com/maps/documentation/geocoding/start#GeocodingRequests
  Haversine formula to calculate the distance: https://en.wikipedia.org/wiki/Haversine_formula, https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206#21623206
