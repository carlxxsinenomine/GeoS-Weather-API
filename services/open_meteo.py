from typing import Optional, Any, Dict

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

URL = "https://api.open-meteo.com/v1/forecast"


def get_current_weather(lat, long) -> Dict[str, Any]:
    # https://open-meteo.com/en/docs?current=precipitation,temperature_2m,rain,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,pressure_msl,apparent_temperature,relative_humidity_2m&daily=weather_code,precipitation_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,rain_sum&timezone=Asia%2FTokyo&hourly=temperature_2m,precipitation_probability,rain,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_speed_180m,wind_direction_10m,wind_direction_80m,wind_direction_120m,wind_direction_180m,wind_gusts_10m,temperature_80m,temperature_120m,temperature_180m,pressure_msl,surface_pressure
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    params = {
        "latitude": lat,
        "longitude": long,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
        ],
        "timezone": "auto",
    }

    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]
    current = response.Current()
    return {'temp_2m': current.Variables(0).Value(),
            'relative_humid_2m': current.Variables(1).Value(),
            'apparent_temp': current.Variables(2).Value(),
            'precipitation': current.Variables(3).Value(),
            'rain': current.Variables(4).Value(),
            'weather_code': current.Variables(5).Value()}


def get_hourly_weather(lat, long) -> Dict[str, Any]:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "precipitation_probability",
            "rain",
            "weather_code",
        ],
        "timezone": "auto",
    }

    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]
    hourly = response.Hourly()

    return {'temp_2m': hourly.Variables(0).Value(),
            'relative_humid_2m': hourly.Variables(1).Value(),
            'apparent_temp': hourly.Variables(2).Value(),
            'precipitation': hourly.Variables(3).Value(),
            'precipitation_prob': hourly.Variables(4).Value(),
            'rain': hourly.Variables(5).Value(),
            'weather_code': hourly.Variables(6).Value()}


def get_daily_weather(lat, long) -> Dict[str, Any]:
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    params = {
        "latitude": lat,
        "longitude": long,
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "precipitation_sum",
            "precipitation_hours",
            "precipitation_probability_max",
        ],
        "timezone": "auto",
    }

    responses = openmeteo.weather_api(URL, params=params)
    response = responses[0]
    daily = response.Daily()

    return {
        'weather_code': daily.Variables(0).Value(),
        'temp_2m_max': daily.Variables(1).Value(),
        'temp_2m_min': daily.Variables(2).Value(),
        'apparent_temp_max': daily.Variables(3).Value(),
        'apparent_temp_min': daily.Variables(4).Value(),
        'precipitation_sum': daily.Variables(5).Value(),
        'precipitation_hours': daily.Variables(6).Value(),
        'precipitation_prob_max': daily.Variables(7).Value()
    }