from straeto import api
import time
import os
from mpl_toolkits.basemap import Basemap
import pickle

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

def getMap(region='reykjavik', res='i', linewidth=0.35, dump=True,
            color='lightgrey', lake_color='#a7cdf2'):
    region = region.lower(); res = res.lower()
    pickle_name = 'map-{}-{}-{}.pickle'.format(region, res, linewidth)

    #Load cached map if it exists
    if os.path.exists(pickle_name):
        map = pickle.load(open(pickle_name, 'rb'))
        return map
    
    if region == 'reykjavik':
        urcrnrlat=64.174820; urcrnrlon=-21.662913
        llcrnrlat=64.054223; llcrnrlon=-22.075822
    elif region == 'iceland':
        urcrnrlat=66.8; urcrnrlon=-12.9
        llcrnrlat=63.2; llcrnrlon=-25
    else:
        raise Exception('Error: Bad region')

    map = Basemap(projection='merc', resolution=res,
              urcrnrlat=urcrnrlat,urcrnrlon=urcrnrlon,
              llcrnrlat=llcrnrlat, llcrnrlon=llcrnrlon)
    map.drawcoastlines(linewidth=linewidth)
    map.fillcontinents(color=color, lake_color=lake_color)
    map.drawmapboundary(fill_color=lake_color)

    if dump:
        pickle.dump(map,
                    open(pickle_name, 'wb'),
                    -1) # Format?
    return map