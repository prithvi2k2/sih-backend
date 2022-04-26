from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class Location:
    def __init__(self, param) -> None:
        if type(param) == str:
            self.location = self.findGeocode(param)
            if self.location:
                self.latitude = self.location.latitude
                self.longitude = self.location.longitude
        else:
            self.location=True
            self.latitude = param[0]
            self.longitude = param[1]

    def findGeocode(self, city):
        try:
            geolocator = Nominatim(user_agent="your_app_name")
            return geolocator.geocode(city)
        except GeocoderTimedOut:
            return self.findGeocode(city)

    def assigned(self, list):
        pass

    def __repr__(self):
        if self.location:
            return [self.longitude, self.latitude]
        return False
