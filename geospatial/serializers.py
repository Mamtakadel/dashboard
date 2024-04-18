
from rest_framework import serializers
from geospatial.models import  PalikaUpload, PalikaGeometry 



class  palikaUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalikaUpload
        fields = '__all__'


class  palikaGeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PalikaGeometry
        fields = '__all__'

