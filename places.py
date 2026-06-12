import httpx

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

CATEGORY_QUERIES = {
    "sleep": [
        'node["tourism"="hotel"](around:3000,{lat},{lon});',
        'node["tourism"="hostel"](around:3000,{lat},{lon});',
        'node["tourism"="motel"](around:3000,{lat},{lon});'
    ],
    "food": [
        'node["amenity"="restaurant"](around:3000,{lat},{lon});',
        'node["amenity"="cafe"](around:3000,{lat},{lon});',
        'node["shop"="supermarket"](around:3000,{lat},{lon});'
    ],
    "general": [
        'node["amenity"="restaurant"](around:3000,{lat},{lon});',
        'node["tourism"="hotel"](around:3000,{lat},{lon});',
        'node["shop"="supermarket"](around:3000,{lat},{lon});'
    ],
}


async def search_places(lat: float, lon: float, category: str):
    queries = CATEGORY_QUERIES.get(category, CATEGORY_QUERIES["general"])

    q_parts = "\n".join(q.format(lat=lat, lon=lon) for q in queries)
    overpass_query = f"""
    [out:json];
    (
    {q_parts}
    );
    out center 5;
    """
    headers = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"
    }

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.get(OVERPASS_URL, params={"data": overpass_query}, headers=headers)
        except Exception as e:
            print(f"Overpass request error: {e}")
            return []

        if resp.status_code != 200:
            print(f"Overpass non-200 status: {resp.status_code}")
            return []

        try:
            data = resp.json()
        except Exception as e:
            print(f"Overpass JSON decode error: {e} - response text: {resp.text[:200]}")
            return []

    places = []
    for el in data.get("elements", [])[:5]:
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("operator") or "Nomi ko'rsatilmagan"
        lat_p = el.get("lat") or (el.get("center") or {}).get("lat")
        lon_p = el.get("lon") or (el.get("center") or {}).get("lon")
        places.append({"name": name, "lat": lat_p, "lon": lon_p})

    return places
