import httpx
import math

async def geocode(address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "DistanceQueryApp/1.0"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception("Geocoding service failure")
        data = response.json()
        if not data:
            return None
        return float(data[0]['lat']), float(data[0]['lon'])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
