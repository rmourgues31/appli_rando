from fastapi import FastAPI
from service import get_alti_from_lonlat

app = FastAPI()

@app.post("/alti/")
def get_alti(lonlat: list[tuple[float, float]]) -> list[int]:
    return get_alti_from_lonlat(lonlat)