from straeto import api
import time

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