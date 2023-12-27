#uploading, reaching, cutting & saving
import numpy as np
import pickle
import pandas as pd

#files paths:
centersfile_path = r"C:\Users\HP\school\MSc\research\cyclone_centers_and_tracks\centers_ERA5_1.25__psl_rsmooth_1958010100-2019123118_1_removed.pkl"
id2track_path = r"C:\Users\HP\school\MSc\research\cyclone_centers_and_tracks\cyclone_to_track_index_ERA5_1.25_rsmooth1958010100-2019123118_1_alpha3.9beta208.0.pkl"
id2track2_path = r"C:\Users\HP\school\MSc\research\cyclone_centers_and_tracks\tracklist_ERA5_1.25_rsmooth1958010100-2019123118_1_alpha3.9beta208.0.pkl"

#loading:
with open(centersfile_path, 'rb') as file:
    centers = pickle.load(file)
with open(id2track_path, 'rb') as file1:
    id2track = pickle.load(file1)
with open(id2track2_path, 'rb') as file2:
    id2track2 = pickle.load(file2)

#exploring centers:
#print(centers.info)
#print(centers.dtypes)

#Getting from time:

print(centers.head())      # centers columns are: ['time', 'lat', 'lon', 'field[m^2/s^2]', 'rad[grid points]','depth[m^2/s^2]', 'vor[1/s]*10^5']
input("1")
#print(id2track.head())     # id2track looks like: cyclone_index(as id), cyclone index, track_index
#print(id2track2.head())    # id2track2 is the track number with a list of the related lows like:   4             [4, 16]

print(type(centers['time'][10])) #<class 'pandas._libs.tslibs.timestamps.Timestamp'>
print(centers['time'][10])       #1958-01-01 06:00:00
timestamp = centers['time'][10]
year = timestamp.year
month = timestamp.month
day = timestamp.day
hour = timestamp.hour
minute = timestamp.minute
second = timestamp.second
print(year, month, day, hour, minute, second ) #ints

#filtering for only DJF
DJF_centers = centers[centers['time'].dt.month.isin([1, 2, 12])]
#print(DJF_centers.head())
#saving filtered file
#DJF_centers.to_csv(r"C:\Users\HP\school\MSc\research\cyclone_centers_and_tracks\DJF_cyclones.csv", index=False)

#taking lows between lons:27.5-40 lats: 32-37
DJF_Cyprus_lows = DJF_centers[(DJF_centers['lat'] >= 32) & (DJF_centers['lat'] <= 37) & (DJF_centers['lon'] >= 27.5) & (DJF_centers['lon'] <= 40)]
# print(DJF_Cyprus_lows['field[m^2/s^2]'].head(10))
# print(DJF_Cyprus_lows.dtypes)
# DJF_Cyprus_lows.to_pickle(r"C:\Users\HP\school\MSc\research\cyclone_centers_and_tracks\DJF_Cyprus_lows.pkl")

input("want to proceed?")


#reaching selected's index and other values by year,month and day for example
# for index, value in DJF_Cyprus_lows['time'].iteritems():
#     a=DJF_Cyprus_lows.loc[DJF_Cyprus_lows['time'] == value, ['lat','lon']]
#     b = DJF_Cyprus_lows.loc[DJF_Cyprus_lows['time'] == value,'lat'] #pd series, can be ndarray with .values
#     c= b.values
#     input("") #stopping
#     #if value.year == 1958 and value.month ==1 and value.day == 2  : print(f"Index: {index}, Time: {value}", a ,b.values)

