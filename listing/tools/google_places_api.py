import os
import requests
import json
from langchain_core.tools import tool
from langchain_community.tools import GooglePlacesTool

@tool
def get_place_id(query: str) -> str:
    """Ottiene l'ID di un luogo a partire dal suo nome e posizione."""
    places = GooglePlacesTool()
    res = places.run(query)
    return res

@tool
def search_places(query: str) -> dict:
    """Cerca luoghi utilizzando una query di testo."""
    api_key = os.getenv("GPLACES_API_KEY")
    if not api_key:
        raise ValueError("API key non trovata nelle variabili d'ambiente")
    
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "*"
    }
    data = {"textQuery": query}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

@tool
def get_place_details(place_id: str) -> dict:
    """Ottiene i dettagli di un luogo specifico dato il suo place_id."""
    api_key = os.getenv("GPLACES_API_KEY")
    if not api_key:
        raise ValueError("API key non trovata nelle variabili d'ambiente")
    
    url = f"https://places.googleapis.com/v1/places/{place_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "*"
    }
    
    response = requests.get(url, headers=headers)
    
    print(response)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

@tool
def get_latitude_longitude(place_id: str) -> dict:
    """Ottiene la latitudine e longitudine di un luogo specifico dato il suo place_id."""
    details = get_place_details(place_id)
    try:
        latitudine = details['location']['latitude']
        longitudine = details['location']['longitude']
        return {
            "latitude": latitudine,
            "longitude": longitudine
        }
    except (KeyError, IndexError) as e:
        print(f"Errore nell'es trazione dei dati: {e}")
        return {
            "latitude": None,
            "longitude": None
        }

@tool
def get_near_places(
    latitude: float,
    longitude: float,
    included_types: list = [
            "parking",
            "electric_vehicle_charging_station",
            "corporate_office",
            "historical_place",
            "preschool",
            "primary_school",
            "secondary_school",
            "university",
            "park",
            "hospital",
            "supermarket",
        ],
    radius: float = 2000.0,
    max_result_count: int = 10
) -> dict:
    """
    Ottiene luoghi specifici nelle vicinanze di una posizione specificata.
    """
    api_key = os.getenv("GPLACES_API_KEY")
    if not api_key:
        raise ValueError("API key non trovata nelle variabili d'ambiente")

    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName"
    }
    data = {
        "includedTypes": included_types,
        "maxResultCount": max_result_count,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
