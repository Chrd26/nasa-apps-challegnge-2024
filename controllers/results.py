
from flask import Flask
from flask import render_template, request
import openeo
import os
from geopy.geocoders import Nominatim
from openeo.processes import ProcessBuilder

class Results:
    def __init__(self, location):
        
        if os.path.exists("./static/result.tiff"):
            self.DeletePicture()

        locator = Nominatim(user_agent='Drought History')
        location =locator.geocode(location)

        self.isLocationFound = True
        if not location:
            self.isLocationFound = False
            return

        print(location.latitude, location.longitude)
        width = location.longitude + 0.3
        height =location.latitude + 0.15

        connection = openeo.connect("openeo.dataspace.copernicus.eu")
        getConnections = connection.list_collection_ids()
        print(getConnections)

        # band combination sentinel 2
        # https://gisgeography.com/sentinel-2-bands-combinations/

        connection.describe_collection("SENTINEL2_L2A")
        connection.authenticate_oidc()
        datacube = connection.load_collection(
        "SENTINEL2_L2A",
        spatial_extent={"west": location.longitude, 
                        "south": location.latitude, 
                        "east": width, "north": height},
        temporal_extent = ["2021-02-01", "2021-04-30"],
        bands=["B11", "B02", "B08"],
        max_cloud_cover = 20)

        swir1 = datacube.band("B11") * 0.0001
        nir = datacube.band("B08") * 0.0001
        blue = datacube.band("B02") * 0.0001

        evi_cube = (nir - swir1) / (nir + swir1 * blue)
        evi_composite = evi_cube.max_time()

        evi_composite.download("./static/result.tiff")
        # evi_composite.execute_batch()

    def DeletePicture(self):
        os.remove("./static/result.tiff")


