import xarray as xr
import numpy as np
import os

pv_folder_path = r'C:\Users\HP\school\MSc\research\Codes\try\pv'
pv_all_files = os.listdir(pv_folder_path)
pv_djf_files = [file for file in pv_all_files if file[-8:-6] in ['12', '01', '02']]
for file_name in pv_djf_files:
    full_path = os.path.join(pv_folder_path, file_name) # Construct the full path to the file

    #shapefile_path1 = "C:/Users/HP/school/MSc/research/Codes/pv_6hrPTlev_reanalysis_ERA5_1992-02-01_1992-02-29.nc"  # Replace with the path to the NetCDF shapefile

    ipv=xr.open_dataset(full_path)

    longitude_range = slice(0, 50)  # Replace lon_start and lon_end with your desired range
    latitude_range = slice(60, 25)

    pv320= ipv.sel(longitude=longitude_range, latitude=latitude_range,level=320) #for pv

    #print(pv320.variables)  # Display the variables in the dataset
    #print(gph925.variables)
    #print(pv320.info()) # Display detailed information about the dataset
    #print(gph925.info())
    #print(pv320.keys())     # Display the variable names in the dataset


    pv320.to_netcdf(pv_folder_path+'CUT\CUT'+ file_name) # Save the subsetted dataset

z_folder_path = r'C:\Users\HP\school\MSc\research\Codes\try\z'
z_all_files = os.listdir(z_folder_path)
z_djf_files = [file for file in z_all_files if file[-7:-5] in ['12', '01', '02']]
for file_name in z_djf_files:
    full_path = os.path.join(z_folder_path, file_name)  # Construct the full path to the file

    # shapefile_path2 = "C:/Users/HP/school/MSc/research/Codes/z_6hrPlev_reanalysis_ERA5_19920201_19920229.nc"

    igph = xr.open_dataset(full_path)

    longitude_range = slice(0, 50)  # Replace lon_start and lon_end with your desired range
    latitude_range = slice(60, 25)

    gph925 = igph.sel(longitude=longitude_range, latitude=latitude_range, level=925)  # for pressure

    gph925.to_netcdf(z_folder_path+'CUT\CUT'+ file_name)