# The following code: (for each nc file seperatelly)
# imports a nc file from and cuts the wanted lon-lat bounderies

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from colorbar import create_brighter_green_cmap
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from scipy.ndimage import label, maximum_filter
import datetime
import pickle
import pandas as pd

# files paths
#shapefile_path = "C:/Users/HP/school/MSc/research/Codes/pv_6hrPTlev_reanalysis_ERA5_2006-01-01_2006-01-31CUT.nc"  # Replace with the path to the NetCDF shapefile
#shapefile_path2 = "C:/Users/HP/school/MSc/research/Codes/z_6hrPlev_reanalysis_ERA5_20060101_20060131CUT.nc"
shapefile_path = "C:/Users/HP/school/MSc/research/Codes/pv_6hrPTlev_reanalysis_ERA5_1992-02-01_1992-02-29CUT.nc"  # Replace with the path to the NetCDF shapefile
shapefile_path2= "C:/Users/HP/school/MSc/research/Codes/z_6hrPlev_reanalysis_ERA5_19920201_19920229CUT.nc"
centersfile_path = r"C:\Users\HP\school\MSc\research\cyclone_centers_and_tracks\DJF_Cyprus_lows.pkl"
count = 249=  # for saving maps mnually
ids = xr.open_dataset(shapefile_path)
ids["pv"] *= 1e6  # units to PVU
custom_cmap = create_brighter_green_cmap()
igph925 = xr.open_dataset(shapefile_path2)
# print(ids)
# centersfile= pd.read_csv(centersfile_path)
with open(centersfile_path, 'rb') as file:
    centersfile = pickle.load(file)
Lcentersfile=centersfile.groupby('time')['lat', 'lon'].agg(list)
CentersList = xr.Dataset.from_dataframe(Lcentersfile)
# print(centersfile.info)
# print(centersfile.dtypes)
#print(centersfile.head())
# print(centersfile.head(10).iloc[:, :4])
times = ids['time']


for time in times:
    #if str(time.values)[8:10] in ['11', '12', '13']:
    # creating the pv map, it's latidudional gradient and it's laplacian
    ds = ids.sel(time=time)  # selecting from pvcenter = {Dataset: 2} <xarray.Dataset>\nDimensions:  ()\nCoordinates:\n    time     datetime64[ns] 2006-01-11\n    level    int32 ...\nData variables:\n    lat      object [33.75]\n    lon      object [30.0]
    gph925 = igph925.sel(time=time)
    aa=CentersList['time'].values[0]
    if  any(CentersList['time'] == time):
        center = CentersList.sel(time=time)
        # Define the coordinates of the point you want to find the nearest maximum for
        target_longitude = center['lon'].values.tolist()[0]
        target_latitude = center['lat'].values.tolist()[0]
        PlotLow=True
    else:
        target_longitude = 35
        target_latitude = 35
        PlotLow=False
    # print(type(ds)) #<class 'xarray.core.dataset.Dataset'>
    lat_grad_ds = ds["pv"].differentiate('longitude')
    lapl_ds = ds["pv"].differentiate('latitude').differentiate('latitude') + ds["pv"].differentiate(
        'longitude').differentiate('longitude')

    # finding all local maxima in map
    pv_array = ds['pv'].values  # Extract the 'pv' variable as a NumPy array
    local_maxima = maximum_filter(pv_array,
                                  size=5)  # Apply a maximum filter to find local maxima (Adjust 'size' as needed)
    maxima_mask = (local_maxima == pv_array)
    # plt.contour(ds['longitude'].values, ds['latitude'].values, maxima_mask, levels=[0.5], colors='yellow', linestyles='solid') # activate to overlay the local maxima on the plot
    # labeled_maxima, num_features = label(local_maxima) # Find connected components and label them (dont remember what this does)


    # finding nearest local maximum to target
    lon_diff = ds[
                   'longitude'].values - target_longitude  # Calculate the differences between the target point and all longitudes and latitudes
    lat_diff = ds['latitude'].values - target_latitude
    distances_squared = lat_diff[:, np.newaxis] ** 2 + lon_diff[np.newaxis,
                                                       :] ** 2  # Calculate the distances squared
    distances_squared[
        maxima_mask == False] = np.inf  # Mask the distances using the labeled_maxima to select only local maxima points
    nearest_max_index = np.unravel_index(np.argmin(distances_squared),
                                         distances_squared.shape)  # Find the indices of the nearest local maximum
    nearest_max_latitude = ds['latitude'].values[
        nearest_max_index[0]]  # Get the longitude and latitude coordinates of the nearest maximum
    nearest_max_longitude = ds['longitude'].values[nearest_max_index[1]]

    # Plotting:
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # Plot original dataset with geographical boundaries using Basemap
    ax[0].set_title('Original Dataset with Geo Boundaries')
    m1 = Basemap(projection='cyl', llcrnrlon=0, llcrnrlat=25, urcrnrlon=50, urcrnrlat=60, ax=ax[0])
    m1.drawcoastlines(linewidth=0.8)
    m1.drawparallels(np.arange(25., 60., 5.), labels=[1, 0, 0, 0], linewidth=0.1)
    m1.drawmeridians(np.arange(0., 50., 5.), labels=[0, 0, 0, 1], linewidth=0.1)
    x, y = m1(ds['longitude'].values, ds['latitude'].values)
    pcm = m1.pcolormesh(x, y, ds["pv"].values, cmap=custom_cmap, shading='auto', vmin=-2,
                        vmax=12)  # setting the scale
    contour_lines = ax[0].contour(x, y, gph925['z'].values, levels=20, colors='black', linewidths=0.5)
    if PlotLow:
        circle = plt.Circle((nearest_max_longitude, nearest_max_latitude), radius=1, color='yellow', fill=False,
                            linestyle='dashed', linewidth=2, alpha=1.0)
        ax[0].add_patch(circle)
        dot_x, dot_y = m1(target_longitude, target_latitude)
        dot_x, dot_y = m1(target_longitude, target_latitude)
        m1.plot(dot_x, dot_y, 'o', color='yellow', markersize=8, markeredgecolor='black')
    ax[0].clabel(contour_lines, inline=True, fontsize=4)
    norm = Normalize(vmin=-2, vmax=12)
    cbar = plt.colorbar(pcm, ax=ax[0], orientation='horizontal', pad=0.05)
    cbar.set_label('PVU')

    # Plot gradient along 'lat' with geographical boundaries using Basemap
    ax[1].set_title('Gradient along Lon with Geo Boundaries')
    m2 = Basemap(projection='cyl', llcrnrlon=0, llcrnrlat=25, urcrnrlon=50, urcrnrlat=60, ax=ax[1])
    m2.drawcoastlines(linewidth=0.8)
    m2.drawparallels(np.arange(25., 60., 5.), labels=[1, 0, 0, 0], linewidth=0.1)
    m2.drawmeridians(np.arange(0., 50., 5.), labels=[0, 0, 0, 1], linewidth=0.1)
    x, y = m2(ds['longitude'].values, ds['latitude'].values)
    pcm1 = m2.pcolormesh(x, y, lat_grad_ds.values, cmap=custom_cmap, shading='auto', vmin=-5 , vmax=5)
    ax[1].clabel(contour_lines, inline=True, fontsize=4)
    cbar1 = plt.colorbar(pcm1, ax=ax[1], orientation='horizontal', pad=0.05)
    cbar1.set_label('Grad')

    # Plot Laplacian with geographical boundaries using Basemap
    ax[2].set_title('Laplacian with Geo Boundaries')
    m3 = Basemap(projection='cyl', llcrnrlon=0, llcrnrlat=25, urcrnrlon=50, urcrnrlat=60, ax=ax[2])
    m3.drawcoastlines(linewidth=0.8)
    m3.drawparallels(np.arange(25., 60., 5.), labels=[1, 0, 0, 0], linewidth=0.1)
    m3.drawmeridians(np.arange(0., 50., 5.), labels=[0, 0, 0, 1], linewidth=0.1)
    x, y = m3(ds['longitude'].values, ds['latitude'].values)
    pcm2 = m3.pcolormesh(x, y, lapl_ds.values, cmap=custom_cmap, shading='auto', vmin=-5,
                        vmax=5)
    ax[2].clabel(contour_lines, inline=True, fontsize=4)
    cbar2 = plt.colorbar(pcm2, ax=ax[2], orientation='horizontal', pad=0.05)
    cbar2.set_label('Lapl')
    plt.suptitle(str(time.values)[:13], fontsize=16)

    for a in ax:
        a.grid(False)
    # plt.show()
    # Saving figs
    plt.savefig(r"C:\Users\HP\school\MSc\research\Codes\maps\1stTry\ " + str(count) + ".jpg", format="png")
    plt.close()
    count += 1

## next tasks:
# 1) get lon&lat of low from amit's data per date and change the target to it
# 5)unify colorbar for all pics for all times
# lons:27.5-40 lats: 32-37
# arrange the code such that you can select dates(also hours) and print/save

# find a way to reach data straight from carbon

## 2nd level-data analysis: analyse grad and lapl
# 1) make maps of full seasons to explore the color scale, then set a constant one
