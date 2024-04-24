
import json
from urllib import request, response
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework import viewsets
from geospatial.models import PalikaUpload, PalikaGeometry, WeatherForecast
from geospatial.serializers import palikaUploadSerializer,palikaGeometrySerializer,WeatherForecastSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import  APIView
from rest_framework.response import Response
from geopandas import geopandas  as gpd
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import zipfile
import os
import glob
from geospatial.task import upload_geojson
import openmeteo_requests
# import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta
    
class UploadData(viewsets.ModelViewSet):
    serializer_class = palikaUploadSerializer
    queryset= PalikaUpload.objects.all()
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request):
        serializer = palikaUploadSerializer(data=request.data)
        print("==================== serializer =-===========", serializer)
        file = request.data.get('file')
        file_type=request.data.get('file_type')
        filename=file.name
        try:
            if serializer.is_valid():
                palika = serializer.save()
                if filename.endswith('.zip'):
                    if file_type=="shapefile":
                        print("INSIDE IF")
                        task=upload_geojson.delay(palika.id)
                        #tasks=upload_geojson(palika.id)
                        print("asdfghjkhgfdfgh",task)
                        return Response("data is uploading")
                elif filename.endswith('.geojson'):
                    gdf = gpd.read_file(palika.file.path)
                    for index, row in gdf.iterrows():
                        geom = GEOSGeometry(str(row['geometry']))
                        attr_data = row.drop('geometry').to_dict()
                        district = attr_data.pop("DISTRICT")
                        ward_number = attr_data.pop("new_ward_n")
                        
                        bbox=geom.extent
                        area_gdf = gpd.GeoDataFrame(geometry=[row["geometry"]], crs=gdf.crs)
                        area_gdf.to_crs(epsg=3857, inplace=True)
                        area = area_gdf.area.iloc[0] / 1000000
                        PalikaGeometry.objects.create(geom=geom,attr_data=attr_data,bbox=bbox,district=district,area=area,ward_number=ward_number,palika=palika)
                    return Response('geojson file uploaded successfully')
                else:
                    return Response('No shapefile provided')
        except Exception as e:
            return Response(f'Error uploading shapefile: {str(e)}')
        

class GetData(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = PalikaGeometry.objects.all()
    serializer_class = palikaGeometrySerializer
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated] 

    def list(self, request):
        ward_no = request.GET.get('ward_no')
        if ward_no:
            data= PalikaGeometry.objects.filter(ward_number=ward_no)
        else:
            data=PalikaGeometry.objects.all()
        data_json =serialize('geojson',data, geometry_field="geom")
        data_json=json.loads(data_json)
        return Response(data_json)
        
class DownloadPalika(viewsets.ModelViewSet):
    parser_classes=[MultiPartParser, FormParser]
    queryset=PalikaGeometry.objects.all()
    serializer_class= palikaGeometrySerializer
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]

    def list(self,request):
        query =PalikaGeometry.objects.all()
        geojson_data = serialize('geojson', query, geometry_field='geom')
        response = HttpResponse(geojson_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="data.geojson"'
        return response

class DownloadWard(viewsets.ModelViewSet):
    parser_classes =[MultiPartParser,FormParser]
    queryset = PalikaGeometry.objects.all()
    serializer_class = palikaGeometrySerializer
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]

    def list(self,request):
        ward_no =request.GET.get('ward_no')
        data = PalikaGeometry.objects.filter(ward_number =ward_no)
        if not data:
            return HttpResponse("No data found for the specified ward number.", status=404)
        else:
            data_json = serialize('geojson',data,geometry_field='geom')
            data_json=json.loads(data_json)
            response = JsonResponse(data_json, safe=False)
            response['Content-Disposition'] = 'attachment; filename="data.geojson"'
            return response



from rest_framework.decorators import api_view
from celery.result import AsyncResult


@api_view(["POST"])
def check_status(request):
    result = AsyncResult(request.data.get("task_id"))
    response_data = {
        'task_id': request.data.get("task_id"),
        'status': result.status,
        'result': result.result,
    }
    return JsonResponse(response_data)


############################################  Current Weather API #####################################################################
class WeatherApi(APIView):
    def post(self, request):
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