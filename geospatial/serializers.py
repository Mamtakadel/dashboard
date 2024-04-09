
from rest_framework import serializers
from geospatial.models import GeoSpatialData, PalikaUpload, PalikaGeometry 

class  GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSpatialData
        fields = ('id', 'username', 'palika_name', 'user', 'geom',  'file_type', 'description', 'data_file', 'upload_date')

class  palikaUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalikaUpload
        fields = '__all__'

class  palikaGeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PalikaGeometry
        fields = '__all__'

# class  GeoJsonDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GeoJsonData
#         fields = '__all__'   

# class  JsonUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JsonUpload
#         fields = '__all__'        

# class  JsonGeometrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JsonGeometry
#         fields = '__all__'        