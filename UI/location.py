from plyer import gps
from plyer.utils import platform

class Locate:
    def locate_gps(self):
        gps.configure(on_location=self.gps_locate)
        gps.start()

    def gps_locate(self, **kwargs):
        lat = kwargs["lat"]
        lon = kwargs["lon"]
        return lat, lon
