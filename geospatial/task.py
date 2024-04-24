
# tasks.py
from celery import shared_task
from .models import PalikaGeometry

from rest_framework.response import Response
from geopandas import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry
from geospatial.models import PalikaUpload


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