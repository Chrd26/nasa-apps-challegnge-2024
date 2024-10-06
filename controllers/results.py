from flask import Flask
from flask import render_template, request
import openeo
import os
from geopy.geocoders import Nominatim

class Results:
    def __init__(self, location):
        locator = Nominatim(user_agent='Drought History')
        location =locator.geocode(location)
        print(location.latitude, location.longitude)
        width = location.longitude + 0.1
        height =location.latitude + 0.05
        print(location.latitude + location.latitude * 0.0001, location.longitude + location.longitude * 0.0001)
        self.isLocationFound = True

        if not location:
            self.isLocationFound = False
            return

        connection = openeo.connect("openeo.dataspace.copernicus.eu")
        getConnections = connection.list_collection_ids()
        print(getConnections)

        connection.describe_collection("SENTINEL2_L2A")
        connection.authenticate_oidc()
        datacube = connection.load_collection(
        "SENTINEL2_L2A",
        spatial_extent={"west": location.longitude, 
                        "south": location.latitude, 
                        "east": width, "north": height},
        temporal_extent = ["2021-02-01", "2021-04-30"],
        bands=["B02", "B04", "B08"])

        blue = datacube.band("B02")
        red =  datacube.band("B04")
        nir =  datacube.band("B08")

        evi_cube = blue * 2

        evi_composite = evi_cube.max_time()
        evi_composite.download("result.tiff")
        # evi_composite.execute_batch()

    def DeletePicture():
        os.remove("result.tiff")
