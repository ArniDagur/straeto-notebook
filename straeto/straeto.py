from straeto import api
import time
import os

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat

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

def get_map(region=None, projection=ccrs.Mercator(),
            res='i', figsize=(8,10)):
    # Map boundaries are specified
    if region == 'reykjavik':
        ur_lat, ur_lon = 64.174820, -21.662913
        ll_lat, ll_lon = 64.054223, -22.075822
        extent = [ur_lon, ll_lon, ur_lat, ll_lat]
    elif region == 'iceland':
        ur_lat, ur_lon = 66.8, -12.9
        ll_lat, ll_lon = 63.2, -25
        extent = [ur_lon, ll_lon, ur_lat, ll_lat]
    elif isinstance(region, list) and len(region) == 4:
        # Region is given in the form [x0, x1, y0, y1]
        extent = region
    elif region != None:
        raise Exception('Error: Bad region')
    
    fig, ax = plt.subplots(figsize=figsize,
                           subplot_kw=dict(projection=projection))
    ax.set_extent(extent) if region != None else False
    
    ax.add_feature(cfeat.GSHHSFeature(scale=res))
    
    return fig, ax