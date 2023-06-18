import requests, json, os, sys
import Backend

path = os.getcwd()
sys.path.append(path)


class ApiConnect:
    payload = None
    headers = None
    dict = {}
    data = None
    temp = None

    def connect_google_api(self, lat, lon):
        # Connect to Google Api
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&types" \
              f"=restaurant&key={Backend.creds.Api_key}"
        response = requests.request("GET", url)
        self.payload = {}
        self.headers = {}
        self.data = json.loads(response.text)
        return self.data["results"]

    def extract(self, res):
        # returns an extraction of api information in a list
        self.temp = []
        for i in res:
            temp_data = {
                "name": i["name"],
                "vicinity": i["vicinity"],
                "rating": i["rating"],
            }

            if "opening_hours" not in i:
                temp_data["open_now"] = "No Info"

            else:
                temp_data["open_now"] = i["opening_hours"]["open_now"]
            self.temp.append(temp_data)
        return self.temp

    def reset(self):
        # Empty the temp dictionary - info obtained from Google api.
        self.temp = {}
        return self.temp

    def __repr__(self):
        # string representation of object
        return json.dumps(self.temp, indent=4)
