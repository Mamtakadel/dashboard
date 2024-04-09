from django.shortcuts import render
from rest_framework import viewsets
from geospatial.models import GeoSpatialData, PalikaGeometry, PalikaUpload
from geospatial.serializers import GeoSerializer,palikaUploadSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from geopandas import geopandas as gpd
from django.contrib.gis.geos import GEOSGeometry
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# from rest_framework.decorators import permission_classes, authentication_classes


class GeoSpatial(viewsets.ModelViewSet):
    queryset = GeoSpatialData.objects.all()
    serializer_class = GeoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        file_type = request.query_params.get("file_type", None)
        if file_type == "True":
            self.queryset = GeoSpatialData.objects.filter(file_type=True)

        else:
            self.queryset = GeoSpatialData.objects.all()
        return super().create(request, *args, **kwargs)



class Geom(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            file = request.data.get("file")
            file_type = request.data.get("file_type")
            if not file_type:
                return Response("File type is required")
            serializer=palikaUploadSerializer(data=request.data)
            if serializer.is_valid():
                obj= serializer.save()
            if file_type=="shapefile":
                gdf = gpd.read_file(file)
                for index, row in gdf.iterrows():
                    geom = GEOSGeometry(str(row["geometry"]))
                    attr_data = row.drop(["geometry"]).to_dict()

                    PalikaGeometry.objects.create(geom=geom, user=request.user,palikaupload=obj)

                return Response("Shapefile uploaded successfully")
            elif file_type=="geojson":
                gdf = gpd.read_file(file)
                #print(gdf)
                for index, row in gdf.iterrows():
                    geom = GEOSGeometry(str(row["geometry"]))
                    #print(geom)
                    attr_data = row.drop(["geometry"]).to_dict()
                    district= attr_data.pop("DISTRICT")
                    state=attr_data.pop ("STATE")
                    #print(district)
                    #print(state)


                    PalikaGeometry.objects.create(geom=geom, user=request.user,palikaupload=obj,district=district,state=state)
                    return Response("Geojson Uploaded Sucessfully")

            
            else:
                return Response("No shapefile or Geojson is provided")
        except Exception as e:
            return Response(f"Error uploading shapefile and Geojson: {str(e)}")
        
class GetData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        palika_geometries= PalikaGeometry.objects.all()
        serializer=palikaUploadSerializer(palika_geometries,many=True)
        return Response(serializer.data)

       
        



# class Geom(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             shp = request.data.get("shp")
#             # return Response('Shapefile Upload sucessfully')

#             if shp:
#                 gdf = gpd.read_file(shp)  # upload
#                 print(gdf)

#                 for index, row in gdf.iterrows():
#                     geom = GEOSGeometry(str(row["geometry"]))
#                     obj = PalikaGeometry.objects.create(geom=geom, user=request.user)
#                     serializer = GeoSerializer(obj, many=False)

#                     return Response(serializer.data)
#                 return Response("Shapefile uploaded successfully")
#             else:
#                 return Response("No shapefile provided")
#         except Exception as e:
#             return Response(f"Error uploading shapefile: {str(e)}")