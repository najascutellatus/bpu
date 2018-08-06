import xarray as xr
import numpy.ma as ma
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import geopandas as gpd
from codar_processing.common import create_dir
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from oceans import uv2spdir, spdir2uv
from mpl_toolkits.axes_grid1 import make_axes_locatable

save_dir = '/Users/mikesmith/Documents/projects/bpu/images/'


file = '/Users/mikesmith/Documents/projects/bpu/totals/hudson_south/RU_MARA_20160123T160000Z.nc'
title_str = 'MARACOOS - Hudson South'
shape_file = '/Users/mikesmith/Downloads/NY_Call_Areas_4_4_2018/hudson_south_subset.shp'
sname = 'RU_MARA_20160123T160000Z_hudson_south.png'

# file = '/Users/mikesmith/Documents/projects/bpu/totals/domain/RU_MARA_20160123T160000Z.nc'
# title_str = 'MARACOOS - Unfiltered'
# shape_file = '/Users/mikesmith/Downloads/NY_Call_Areas_4_4_2018/NY_Call_Areas_4_4_2018.shp'
# sname = 'RU_MARA_20160123T160000Z_domain.png'

save_name = os.path.join(save_dir, sname)
leasing_areas = gpd.read_file(shape_file)
leasing_areas = leasing_areas.to_crs(crs={'init': 'epsg:4326'})


regions = dict(maracoos=[-76, -68, 37.5, 42.5])
velocity_min = 0
velocity_max = 60

ds = xr.open_mfdataset(file)

LAND = cfeature.NaturalEarthFeature(
    'physical', 'land', '10m',
    edgecolor='face',
    facecolor='tan'
)

state_lines = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

fig = plt.figure()
sub = 2

for t in ds.time.data:
    # temp = ds.sel(time=t, z=0) # Works with CF/NCEI compliant netCDF files created in 2018
    temp = ds.sel(time=t)
    temp = temp.squeeze()

    timestamp = pd.Timestamp(t).strftime('%Y%m%dT%H%M%SZ')

    for key, values in regions.items():
        extent = values
        tds = temp.sel(
            lon=(temp.lon > extent[0]) & (temp.lon < extent[1]),
            lat=(temp.lat < extent[3]) & (temp.lat > extent[2]),
        )

        u = tds['u'].data
        v = tds['v'].data

        lon = tds.coords['lon'].data
        lat = tds.coords['lat'].data
        time = tds.coords['time'].data

        u = ma.masked_invalid(u)
        v = ma.masked_invalid(v)

        angle, speed = uv2spdir(u, v)
        us, vs = spdir2uv(np.ones_like(speed), angle, deg=True)

        lons, lats = np.meshgrid(lon, lat)

        speed_clipped = np.clip(speed, velocity_min, velocity_max).squeeze()
        np.count_nonzero(~np.isnan(speed))
        fig, ax = plt.subplots(figsize=(11, 8),
                                 subplot_kw=dict(projection=ccrs.PlateCarree()))

        # Plot title
        plt.title('{}\n{} - {}'.format(tds.title, title_str, timestamp))

        # # plot pcolor on map
        # h = ax.imshow(speed_clipped[::sub],
        #               vmin=velocity_min,
        #               vmax=velocity_max,
        #               cmap='jet',
        #               interpolation='bilinear',
        #               extent=extent,
        #               origin='lower')
        areas = leasing_areas.plot(ax=ax, color='white', edgecolor='red')

        # plot arrows over pcolor
        ax.quiver(lons[::sub, ::sub], lats[::sub, ::sub],
                   us[::sub, ::sub], vs[::sub, ::sub],
                   cmap='jet',
                   scale=60)

        # Gridlines and grid labels
        gl = ax.gridlines(draw_labels=True,
                           linewidth=1,
                           color='black',
                           alpha=0.5, linestyle='--')

        gl.xlabels_top = gl.ylabels_right = False
        gl.xlabel_style = {'size': 15, 'color': 'gray'}
        gl.ylabel_style = {'size': 15, 'color': 'gray'}
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        # Axes properties and features
        ax.set_extent(extent)
        ax.add_feature(LAND, zorder=0, edgecolor='black')
        ax.add_feature(cfeature.LAKES)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(state_lines, edgecolor='black')
        save_path = os.path.join(save_dir, key)
        create_dir(save_path)

        # divider = make_axes_locatable(ax)
        # cax = divider.new_horizontal(size='5%', pad=0.05, axes_class=plt.Axes)
        # fig.add_axes(cax)

        # generate colorbar
        # cb = plt.colorbar(h, cax=cax)
        # cb.set_label('cm/s')
        # plt.show()
        fig_size = plt.rcParams["figure.figsize"]
        fig_size[0] = 12
        fig_size[1] = 8.5
        plt.rcParams["figure.figsize"] = fig_size

        plt.savefig(save_name, dpi=300)
        plt.close('all')
        # plt.show()