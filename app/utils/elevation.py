import traceback
import requests
import json
from numpy import diff, maximum
import os

ALTI_URL = "http://" + os.getenv("ALTI_SERVICE") + ":" + os.getenv("ALTI_PORT") + "/alti"

def get_alti(points: list[tuple[float, float]]) -> list[int]:
    '''
    From a list of (lon, lat) points, return list of altitudes
    '''
    try:
        response = requests.post(ALTI_URL, json=points)
        data = json.loads(response.content)
        return data

    except:
        traceback.print_exc()
        return [0]*len(points)
    
def axis_alti(max_alti: int) -> int:
    '''
    Compute the superior limit of y axis for elevation profile graph
    '''
    
    return 500*(int(max_alti/500)+1)
    

def compute_elevation_gain(elev: list[int]) -> int:
    """
    Compute the total elevation gain from a list of altitudes
    """
    return sum(maximum(diff(elev), 0))