
# tasks.py
from celery import shared_task
from .models import PalikaGeometry

from rest_framework.response import Response
from geopandas import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry
from geospatial.models import PalikaUpload, WeatherForecast
import openmeteo_requests
# import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta


# @shared_task()
# def upload_geojson(id):
#     print("This is running", id)
#     obj = PalikaUpload.objects.get(id=id)
#     print(obj)
#     # file=obj.file.path(obj.file_.path)
#     print("================", obj)
#     gdf = gpd.read_file(obj.file)
#     for index, row in gdf.iterrows():
#         #print("============= reached for loop ===========")
#         geom = GEOSGeometry(str(row["geometry"]))
#         attr_data = row.drop(["geometry"]).to_dict()
#         district = attr_data.pop("DISTRICT")
#         ward_number = attr_data.pop("new_ward_n")
#         bbox = geom.extent
#         area_gdf = gpd.GeoDataFrame(geometry=[row["geometry"]], crs=gdf.crs)
#         area_gdf.to_crs(epsg=3857, inplace=True)
#         area = area_gdf.area.iloc[0] / 1000000
#         PalikaGeometry.objects.create(
#             geom=geom,
#             district=district,
#             bbox=bbox,
#             area=area,
#             attr_data=attr_data,
#             ward_number=ward_number,
#             palika=obj,
#         )
#         print("=========================================")

#     return Response ("Completed")

        #return "completed"
###################################### sus################################################
from celery import shared_task
from rest_framework.response import Response
from geopandas import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry

from geospatial.models import PalikaUpload, PalikaGeometry
from dashboard.celery import app


@shared_task
def upload_geojson(id):
    palika= PalikaUpload.objects.get(id=id)
    gdf = gpd.read_file(palika.file)
    
    for index, row in gdf.iterrows():
        geom = GEOSGeometry(str(row["geometry"]))
        print("This is geom",geom)
        attr_data = row.drop(["geometry"]).to_dict()
        district = attr_data.pop("DISTRICT")
        ward_number = attr_data.pop("new_ward_n")
        bbox = geom.extent
        area_gdf = gpd.GeoDataFrame(geometry=[row["geometry"]], crs=gdf.crs)
        area_gdf.to_crs(epsg=3857, inplace=True)
        area = area_gdf.area.iloc[0] / 1000000
        PalikaGeometry.objects.create(
            geom=geom,
            district=district,
            bbox=bbox,
            area=area,
            attr_data=attr_data,
            ward_number=ward_number,
            palika=palika,
        )
        print("*********************************")
    #return palika
################################## Celery Beat #############################################

@shared_task
def weatherpostapi():
    retry_session = retry(retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 27.15,
        "longitude": 85.9,
        "current": ["relative_humidity_2m", "apparent_temperature", "precipitation", "rain"],
        "timezone": "auto",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    current = response.Current()
    current_relative_humidity_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_precipitation = current.Variables(2).Value()
    current_rain = current.Variables(3).Value()
    print(current_apparent_temperature)
    
    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(current.Time(), unit = "s", utc = True),
        end = pd.to_datetime(current.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = current.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = current_apparent_temperature
    hourly_data["relative_humidity_2m"] = current_relative_humidity_2m
    hourly_data["precipitation"] = current_precipitation
    hourly_data["rain"] = current_rain
    
    

    date_value = pd.to_datetime(current.Time(), unit="s") + timedelta(hours=5, minutes=52)

    
    obj = WeatherForecast.objects.create(temperature_2m=float(hourly_data["temperature_2m"]), rain=float(hourly_data["rain"]), 
                                        relative_humidity_2m=float(hourly_data["relative_humidity_2m"]), 
                                        precipitation=float(hourly_data["precipitation"]),date= date_value)
    print(obj)
    print(f"Current time {current.Time()}")
    print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
    print(f"Current apparent_temperature {current_apparent_temperature}")
    print(f"Current precipitation {current_precipitation}")
    print(f"Current rain {current_rain}")
    return Response(WeatherForecast.objects.filter(id=obj.id).values())   