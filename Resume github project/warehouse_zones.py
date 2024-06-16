from shapely import Polygon, contains, Point
import pandas as pd
import json
import math

df_warehouses = pd.read_csv('amazon_warehouses.csv')
df_zipcodes = pd.read_csv('zip_lat_long.csv', dtype={'ZIP':str})

with open('west_region_zone.geojson','r') as f:
    region_geo_fence = json.load(f)

for geometry in region_geo_fence['features']:
    for coords in geometry['geometry']['coordinates']:
        coords # data format: [[long,lat],[long,lat],...]

polygon = Polygon(coords) # western region polygon


def in_region(lat:float,long:float):
    """
    Returns a 1.0 if coordinates given are within the defined region, which is shapely.Polgon object, and 0.0 if they are not.
    Args:
        lat (float): latitude
        long (float): longitude
    """
    if contains(polygon, Point(long, lat)):
        return 1
    else:
        return 0


df_zipcodes['in_region'] = df_zipcodes.apply(lambda x: in_region(x.LAT,x.LNG), axis=1)

df_zipcodes = df_zipcodes[df_zipcodes['in_region']!=0][['ZIP','LAT','LNG']]

df_joined = df_zipcodes.merge(df_warehouses[['Warehouse Name','lat','long']], how='cross')


def haversine(lat1:float, long1:float, lat2:float, long2:float):
    """
    Uses haversine formula to approximate the distance in miles between two coordinate sets
    
    Args:
        lat1 (float): latitude of coordinate 1
        long1 (float): longitude of coordinate 1
        lat2 (float): latitude of coordinate 2
        long2 (float): longitude of coordinate 2
    
    Returns: distance in miles (float)
    """
    R = 3956 # circumfrence of Earth in miles
    dlat = math.radians(lat2 - lat1) # delta phi
    dlong = math.radians(long2 - long1) # delta lambda
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlong/2)**2
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * b


df_joined['distance_mi'] = df_joined.apply(lambda x: haversine(x.LAT,x.LNG,x.lat,x.long), axis=1)

df_joined['rank_distance'] = df_joined.groupby(['ZIP'])['distance_mi'].rank(method='first',ascending=True)

df_joined = df_joined[df_joined['rank_distance']==1.0][['ZIP','Warehouse Name','distance_mi','LAT','LNG']].reset_index(drop=True)

df_joined.to_csv('warehouses_regionalized.csv')