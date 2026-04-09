import requests
import math
from typing import List, Dict, Optional

def fetch_osm_places(query: str, lat: Optional[float] = None, lng: Optional[float] = None, limit: int = 20) -> List[Dict]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": limit
    }
    # If user location provided, strongly bias results towards it
    if lat is not None and lng is not None:
        params["viewbox"] = f"{lng-0.1},{lat+0.1},{lng+0.1},{lat-0.1}"
        # Removing bounded=1 so global searches still work
        
    headers = {
        "User-Agent": "QueueRadarApp/1.0 (MVP)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching OSM data: {e}")
    return []

def extract_place_data(osm_data: Dict) -> Dict:
    address = osm_data.get("address", {})
    city = address.get("city") or address.get("town") or address.get("county") or "Unknown"
    place_type = osm_data.get("type", "unknown")
    
    # Generate clean name
    name = osm_data.get("name")
    if not name:
        name = osm_data.get("display_name", "").split(",")[0]
        
    return {
        "external_id": str(osm_data.get("place_id")),
        "name": name,
        "type": place_type,
        "city": city,
        "lat": float(osm_data.get("lat", 0)),
        "lng": float(osm_data.get("lon", 0))
    }

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Haversine formula in km
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def search_osm_places(query: str, lat: Optional[float] = None, lng: Optional[float] = None, radius_km: Optional[float] = None) -> List[Dict]:
    results = fetch_osm_places(query, lat, lng)
    
    # Fallback for global famous places that get omitted if viewbox is strictly applied
    if not results and lat is not None and lng is not None and not radius_km:
        results = fetch_osm_places(query)
        
    unique_places = []
    seen = set()
    for r in results:
        data = extract_place_data(r)
        
        # Apply strict Haversine radius filter if requested
        if radius_km and lat is not None and lng is not None:
            if data["lat"] and data["lng"]:
                dist = calculate_distance(lat, lng, data["lat"], data["lng"])
                if dist > radius_km:
                    continue
        
        if data["name"] and data["external_id"] not in seen:
            seen.add(data["external_id"])
            unique_places.append(data)
    return unique_places

def get_nearby_osm_places(lat: float, lng: float, category: str = "", limit: int = 15, radius_km: float = 10.0) -> List[Dict]:
    # Query Nominatim natively by category
    query = category if category else "places"
    # Provide strict radius filter so it drops garbage unrelated results out-of-bounds
    results = search_osm_places(query, lat, lng, radius_km=radius_km)
    return results[:limit]

def reverse_geocode(lat: float, lng: float) -> Dict[str, str]:
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lng,
        "format": "jsonv2"
    }
    headers = {
        "User-Agent": "QueueRadarApp/1.0 (MVP)"
    }
    res = {"city": "Unknown Location", "state": "", "country": ""}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            address = data.get("address", {})
            res["city"] = address.get("city") or address.get("town") or address.get("village") or address.get("county") or "Unknown Location"
            res["state"] = address.get("state", "")
            res["country"] = address.get("country", "")
    except Exception as e:
        print(f"Error reverse geocoding: {e}")
    return res
