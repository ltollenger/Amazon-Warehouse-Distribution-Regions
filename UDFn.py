from shapely import Polygon, Point, contains
import math

def in_region(lat:float,long:float, region_coords:list):
    """
    Returns a 1.0 if coordinates given are within the defined region, which is shapely.Polgon object, and 0.0 if they are not.
    Args:
        lat (float): latitude
        long (float): longitude
    """
    region_polygon = Polygon(region_coords)
    if contains(region_polygon, Point(long, lat)):
        return 1
    else:
        return 0

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
