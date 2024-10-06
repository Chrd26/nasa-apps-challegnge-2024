from flask import Flask
from flask import render_template, request
import openeo
import os
from geopy.geocoders import Nominatim

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
        width = location.longitude + 0.6
        height =location.latitude + 0.3

        connection = openeo.connect("openeo.dataspace.copernicus.eu")
        getConnections = connection.list_collection_ids()
        print(getConnections)

        connection.describe_collection("COPERNICUS_PLANT_PHENOLOGY_INDEX")
        connection.authenticate_oidc()
        datacube = connection.load_collection(
        "COPERNICUS_PLANT_PHENOLOGY_INDEX",
        spatial_extent={"west": location.longitude, 
                        "south": location.latitude, 
                        "east": width, "north": height},
        temporal_extent = ["2021-02-01", "2021-04-30"],
        bands=["QFLAG", "PPI"])

        ppi = datacube.band("PPI") * 0.0001
        qflag = datacube.band("QFLAG") * 0.0001

        evi_cube = ppi + qflag

        evi_composite = evi_cube.max_time()
        evi_composite.download("./static/result.tiff")
        # evi_composite.execute_batch()

    def DeletePicture(self):
        os.remove("./static/result.tiff")
