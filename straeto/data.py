import os
from urllib.request import urlretrieve
from zipfile import ZipFile
from subprocess import run

OSM_DATA_URL = 'http://download.geofabrik.de/europe/iceland-latest-free.shp.zip'
OSM_DATA_ZIP_NAME = 'osm-data.zip'
OSM_DATA_DIR_NAME = 'osm-data'

PROJ_PATH = os.path.abspath('..')

def get_osm_data(verbose=False):
    if not os.path.exists(OSM_DATA_ZIP_NAME):
        urlretrieve(OSM_DATA_URL, OSM_DATA_ZIP_NAME)
    with ZipFile(OSM_DATA_ZIP_NAME) as zf:
        extracted_files = 0
        for f in zf.namelist():
            if f.startswith('gis_osm_roads'):
                zf.extract(f, OSM_DATA_DIR_NAME)
                extracted_files += 1
        assert extracted_files == 5, 'Error in number of extracted files: {} != 5'
    r = run([
            PROJ_PATH+'/extract_roads',
            PROJ_PATH+'/osm-data/gis_osm_roads_free_1.shp',
            PROJ_PATH+'/osm-data/output/'
        ])
    assert r.returncode == 0, 'Return code is not 0 (r.returncode={})'.format(r.returncode)
    print('Success') if verbose else False