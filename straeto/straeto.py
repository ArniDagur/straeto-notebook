from straeto import api
import time
import os

PROJ_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def getConsecutiveBuses(ratio=1/2):
    assert 0 <= ratio <= 1

    p_buses = api.getAllBusPositions()

    p_bdict = dict()
    for pb in p_buses:
        p_bdict[pb['deviceNumber']] = {'gpsTime':pb['gpsTime'], 'lat':pb['lat'], 'lon':pb['lon'],
        'speed':pb['speed'], 'route':pb['route']}

    bdict = dict()
    while True:
        buses = api.getAllBusPositions()

        for pb in p_buses:
            did = pb['deviceNumber']
            try:
                b = next(b for b in buses if b['deviceNumber'] == did)
            except:
                # Bus is in first sample but not the latter
                continue
            if ( # Latter sample is not the same as first + speed is above 2
            b['gpsTime'] != pb['gpsTime']
            and b['lat'] != pb['lat'] and b['lon'] != pb['lon']
            and b['speed'] > 2 and pb['speed'] > 2
            ):
                bdict[did] = {'gpsTime':b['gpsTime'], 'lat':b['lat'], 'lon':b['lon'],
                'speed':b['speed'], 'route':b['route']}
        
        if ratio*len(p_bdict) < len(bdict):
            for key in list(p_bdict):
                if key not in bdict:
                    p_bdict.pop(key)
            return bdict, p_bdict

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import numpy as np
from matplotlib.colors import to_rgb

def get_map(region=None, zoom=1, projection=ccrs.Mercator(),
            res='i', land_color='#f0f0f0', ocean_color='#7fcdff', figsize=(8,10)):
    # --  MAP BOUNDARIES  -- #
    assert 0 < zoom, 'Error: Zoom <= 0'
    if region == 'reykjavik':
        ur_lat, ur_lon = 64.174820, -21.662913
        ll_lat, ll_lon = 64.054223, -22.075822
    elif region == 'iceland':
        ur_lat, ur_lon = 66.8, -12.9
        ll_lat, ll_lon = 63.2, -25
    elif isinstance(region, list) and len(region) == 4:
        # Region is given in the form [x0, x1, y0, y1]
        ur_lat, ur_lon = region[2], region[0]
        ll_lat, ll_lon = region[3], region[1]
    elif region != None:
        raise Exception('Error: Bad region')
    if region != None:
        x_offset = ((ur_lon-ll_lon)/2)*(1-(1/zoom))
        y_offset = ((ur_lat-ll_lat)/2)*(1-(1/zoom))
        extent = [ur_lon-x_offset, ll_lon+x_offset, ur_lat-y_offset, ll_lat+y_offset]
    # --  MAP BOUNDARIES /-- #
    
    fig, ax = plt.subplots(figsize=figsize,
                           subplot_kw={
                               # kwargs passed to add_subplot()
                               'projection': projection
                          })
    ax.imshow(np.tile(np.array([[to_rgb(ocean_color)]]), [2, 2, 1]),
            origin='upper',
            transform=ccrs.PlateCarree(),
            extent=[-180, 180, -180, 180]
            )
    ax.set_extent(extent) if region != None else False
    
    ax.add_feature(cfeat.GSHHSFeature(scale=res, facecolor=land_color))
    
    return fig, ax

from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

def add_shapefile(ax, shapefile, projection=ccrs.PlateCarree(),
                  facecolor='none', edgecolor='black'):
    shape_feature = ShapelyFeature(Reader(shapefile).geometries(), projection)
    ax.add_feature(shape_feature, facecolor=facecolor, edgecolor=edgecolor)
    return ax