from utils.elevation import get_alti, compute_elevation_gain
from utils.geo import distance_km

def refresh_spec(coords: list[tuple[float, float]]) -> dict:
    '''
    Compute the spec of the new hike
    Inputs
    - coords: list of (lon, lat) points
    Outputs
    - coordinates: list of (lon, lat) points
    - cum_distance: flattened list of cumulative distance (km) from first point
    - elevation: flattened list of elevations (m)
    - total_dist: end of cum_dist
    '''
    
    if coords is None:
        return {}
    
    else:
        dist = distance_km([f[0:2] for f in coords])
        elev = get_alti(coords)
        elevation_gain = compute_elevation_gain(elev)
        return {
            "cum_distance": dist,
            "coordinates": coords,
            "elevation": elev,
            "total_dist": dist[-1],
            "elevation_gain": elevation_gain
        }