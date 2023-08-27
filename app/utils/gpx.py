import base64
import io
import gpxpy.gpx
from utils.geo import reduce_line

def gpx_from_upload_component(content: str) -> gpxpy.gpx.GPX:
    '''
    Read GPX file from bytes
    '''
    _, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    s = io.BytesIO(decoded)
    return gpxpy.parse(s.read())

def extract_route(gpx_data: gpxpy.gpx.GPX) -> list[tuple[float, float]]:
    '''
    From a GPX file, return the list of (lon, lat) points
    '''

    line = []
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                line.append((point.longitude, point.latitude))
    return reduce_line(line)

def create_gpx(points: list[tuple[float, float]]) -> str:
    '''
    Create a GPX file from (lat, lon) points, and write to file
    '''
    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    # Create points:
    for p in points:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(p[0], p[1]))

    return gpx.to_xml()