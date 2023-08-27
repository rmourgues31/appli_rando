from datetime import datetime
import time

def unix_to_datetime(timestamp: int) -> datetime:
    '''
    Unix timestamp in ms -> datetime object
    '''
    return datetime.fromtimestamp(timestamp/1000)

def datetime_from_iso(iso: str) -> datetime:
    '''
    ISO format datetime -> datetime
    '''
    return datetime.fromisoformat(iso)

def unix_to_hour(timestamp: int) -> str:
    '''
    Unix timestamp in ms -> String HH:MM
    '''
    return datetime_to_hour(unix_to_datetime(timestamp))

def unix_to_fr_date_hour(timestamp: int) -> str:
    '''
    Unix timestamp in ms -> String DD/MM/YYYY - HH:MM
    '''
    return datetime_to_fr_date_hour(unix_to_datetime(timestamp))

def datetime_to_fr_date_hour(dt: datetime) -> str:
    '''
    Datetime -> String DD/MM/YYYY - HH:MM
    '''
    return datetime.strftime(dt, "%d/%m/%Y - %H:%M")

def datetime_to_hour(dt: datetime) -> str:
    '''
    Datetime -> DD/MM/YYYY - String HH:MM
    '''
    return datetime.strftime(dt, "%H:%M")

def unix_to_fr_date_hour(timestamp: int) -> str:
    '''
    Unix timestamp in ms -> String DD/MM/YYYY - HH:MM
    '''
    return datetime_to_fr_date_hour(unix_to_datetime(timestamp))

def seconds_to_hour_min(sec: int) -> str:
    '''
    Seconds -> String Hh Mm
    '''
    _time = time.gmtime(sec)
    if _time.tm_hour == 0:
        return time.strftime('%M min', _time)
    return time.strftime('%H h %M min', time.gmtime(sec))

def iso_to_fr_date_hour(iso: str) -> str:
    '''
    ISO format datetime -> String DD/MM/YYYY -> HH:MM
    '''
    return datetime_to_fr_date_hour(datetime_from_iso(iso))