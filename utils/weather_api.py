"""
Weather and air quality data integration.
Uses free APIs: OpenWeatherMap and OpenAQ.
"""
import requests
from datetime import datetime


# You'll need to sign up for a free API key at openweathermap.org
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your key


def get_weather(lat, lon):
    """Get current weather from OpenWeatherMap."""
    if OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        # Demo data if no API key
        return {
            'temperature': 12.0,
            'humidity': 78,
            'pressure': 1013,
            'wind_speed': 3.2,
            'description': 'Partly cloudy',
            'timestamp': datetime.now().isoformat(),
            'source': 'demo'
        }

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat, 'lon': lon,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        r = requests.get(url, params=params, timeout=10).json()
        return {
            'temperature': r['main']['temp'],
            'humidity': r['main']['humidity'],
            'pressure': r['main']['pressure'],
            'wind_speed': r['wind']['speed'],
            'description': r['weather'][0]['description'],
            'timestamp': datetime.now().isoformat(),
            'source': 'openweathermap'
        }
    except Exception as e:
        return {'error': str(e)}


def get_air_quality(lat, lon):
    """Get air quality from OpenAQ (free, no key needed)."""
    try:
        url = "https://api.openaq.org/v2/latest"
        params = {
            'coordinates': f"{lat},{lon}",
            'radius': 25000,
            'limit': 1
        }
        r = requests.get(url, params=params, timeout=10).json()

        if r.get('results'):
            measurements = r['results'][0].get('measurements', [])
            data = {m['parameter']: m['value'] for m in measurements}
            return {
                'PM25': data.get('pm25'),
                'PM10': data.get('pm10'),
                'NO2': data.get('no2'),
                'O3': data.get('o3'),
                'CO': data.get('co'),
                'timestamp': datetime.now().isoformat(),
                'source': 'openaq'
            }
        return {'info': 'No stations nearby'}
    except Exception as e:
        return {'error': str(e)}


# Danish city coordinates
CITIES = {
    'Copenhagen': (55.6761, 12.5683),
    'Aarhus': (56.1629, 10.2039),
    'Odense': (55.4038, 10.4024),
    'Aalborg': (57.0488, 9.9217),
    'Esbjerg': (55.4765, 8.4594),
    'Randers': (56.4607, 10.0364),
    'Jutland (Central)': (56.0, 9.5),
    'Zealand': (55.5, 11.8),
}
