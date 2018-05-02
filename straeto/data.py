import os
from urllib.request import urlretrieve
from zipfile import ZipFile

OSM_DATA_URL = "http://download.geofabrik.de/europe/iceland-latest-free.shp.zip"
OSM_DATA_ZIP_NAME = "osm-data.zip"
OSM_DATA_DIR_NAME = "osm-data"

def get_osm_data():
    if not os.path.exists(OSM_DATA_ZIP_NAME):
        urlretrieve(OSM_DATA_URL, OSM_DATA_ZIP_NAME)
    with ZipFile(OSM_DATA_ZIP_NAME) as zf:
        for f in zf.namelist():
            if f.startswith("gis.osm_roads"):
                zf.extract(f, OSM_DATA_DIR_NAME)
    # TODO: Make it run extract_roads