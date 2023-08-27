from haversine import haversine, Unit
from simplification.cutil import simplify_coords_vwp

def reduce_line(line: list[tuple[float, float]]) -> list[tuple[float, float]]:
    '''
    Reduce line complexity
    '''

    # 2nd argument is threshold area in coordinates units
    return simplify_coords_vwp(line, 0.00000001)

def distance_km(coords: list[tuple[float, float]]) -> list[float]:
    '''
    Compute a progressive distance list in km for (lon, lat) list of points
    '''
    dist = [0]
    for i in range(1, len(coords)):
        d = haversine(tuple(coords[i-1][::-1]), tuple(coords[i][::-1]), Unit.KILOMETERS)
        dist.append(dist[-1] + d)
    return [round_distance(d*1000) for d in dist]

def round_distance(dist: float) -> float:
    '''
    Round a distance in meter in .1f kilometers
    '''
    return round(dist/1000, 2)

def distance_to_string(dist: float) -> str:
    '''
    Return a distance in meters as a well displayed string
    '''
    if dist >= 1000:
        return str(round_distance(dist)) + " km"
    else:
        return str(int(round_distance(dist) * 1000)) + " m"