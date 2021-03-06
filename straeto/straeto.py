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

def extent_from_region(region):
    if isinstance(region, list) and len(region) == 2:
        zoom = region[1]
        region = region[0]
        assert 0 < zoom, 'Error: Zoom <= 0'
    elif isinstance(region, str) or (isinstance(region, list) and len(region) == 4):
        zoom = 1
    else:
        raise Exception('Error: Bad Region 1')

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
    else:
        raise Exception('Error: Bad region 2')

    x_offset = ((ur_lon-ll_lon)/2)*(1-(1/zoom))
    y_offset = ((ur_lat-ll_lat)/2)*(1-(1/zoom))
    extent = [ur_lon-x_offset, ll_lon+x_offset, ur_lat-y_offset, ll_lat+y_offset]
    return extent
    

def get_map(region=None, zoom=1, projection=ccrs.Mercator(),
            res='i', draw_coastlines=True, figsize=(8,10), shape=(1,1)):
    extents = []
    if isinstance(region, str):
        region = [region]
    for r in region:
        extents.append(extent_from_region(r))

    fig, axes = plt.subplots(shape[0], shape[1], figsize=figsize,
                           subplot_kw={
                               # kwargs passed to add_subplot()
                               'projection': projection
                          })
    if not isinstance(axes, (list, np.ndarray)):
        axes = [axes]
    for ax, e in zip(axes, extents):
        ax.set_extent(e)
        ax.add_feature(cfeat.GSHHSFeature(scale=res)) if draw_coastlines else False
    
    if len(axes) == 1:
        return fig, axes[0]
    else:
        return fig, axes

from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

def add_shapefile(ax, shapefile, projection=ccrs.PlateCarree(),
                  facecolor='none', edgecolor='black'):
    shape_feature = ShapelyFeature(Reader(shapefile).geometries(), projection)
    ax.add_feature(shape_feature, facecolor=facecolor, edgecolor=edgecolor)
    return ax

from scipy.stats import binned_statistic_2d

def add_heatmap(ax, X, Y, Z, bins=50, statistic='mean', cmap='seismic', vmin=0.5, vmax=1.5,
                projection=ccrs.PlateCarree()):
    heatmap, x_edges, y_edges, _ = binned_statistic_2d(X, Y, Z, bins=bins, statistic=statistic)
    extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    im = ax.imshow(heatmap.T, cmap=cmap, vmin=vmin, vmax=vmax,
                   extent=extent, origin='lower', transform=projection)
    return im

from mpl_toolkits.axes_grid1 import make_axes_locatable

def add_colorbar(fig, ax, im, label='', fontsize=20):
    divider = make_axes_locatable(ax)
    cax = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes)
    fig.add_axes(cax)
    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label(label, size=fontsize)

def plot_homes_and_stops(ax):
    ax.plot(-21.949770, 64.086517, marker='o', color='red', markersize=12, transform=ccrs.Geodetic(),
             label='Heimili')
    ax.plot(-21.928427, 64.092127, marker='o', color='red', markersize=12, transform=ccrs.Geodetic())

    ax.plot(-21.950178, 64.085622, marker='o', color='orange', markersize=9, transform=ccrs.Geodetic(),
             label='Strætóstopp')
    ax.plot(-21.929836, 64.092050, marker='o', color='orange', markersize=9, transform=ccrs.Geodetic())
    ax.legend()
    return ax
