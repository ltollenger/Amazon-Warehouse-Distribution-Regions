import UDFn as Fn
import pandas as pd
import json

df_warehouses = pd.read_csv('amazon_warehouses.csv')
df_zipcodes = pd.read_csv('zip_lat_long.csv', dtype={'ZIP':str})

with open('west_region_zone.geojson','r') as f:
    region_geo_fence = json.load(f)

# list of coords to define regional boundary US
for geometry in region_geo_fence['features']:
    for coords in geometry['geometry']['coordinates']:
        coords # data format: [[long,lat],[long,lat],...]

# filter to only coords found in the region coordinate plane
df_zipcodes['in_region'] = df_zipcodes.apply(lambda x: Fn.in_region(x.LAT,x.LNG,region_coords=coords), axis=1)

df_zipcodes = df_zipcodes[df_zipcodes['in_region']!=0][['ZIP','LAT','LNG']]

# cross join all the zip codes to the warehouses (origin points) DataFrame
df_joined = df_zipcodes.merge(df_warehouses[['Warehouse Name','lat','long']], how='cross')

# Use Haversine formula to determine the approximate distance between origin (warehouse) and destination (zipcode) points
df_joined['distance_mi'] = df_joined.apply(lambda x: Fn.haversine(x.LAT,x.LNG,x.lat,x.long), axis=1)

# Rank the zipcodes by closest location
df_joined['rank_distance'] = df_joined.groupby(['ZIP'])['distance_mi'].rank(method='first',ascending=True)

# Filter to only the closest location
df_joined = df_joined[df_joined['rank_distance']==1.0][['ZIP','Warehouse Name','distance_mi','LAT','LNG']].reset_index(drop=True)

# Export df_joined as a CSV file
df_joined.to_csv('warehouses_regionalized.csv')