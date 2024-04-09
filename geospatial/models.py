
from django.db import models

from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismd
from django.core.validators import FileExtensionValidator
# from modeltranslation.translator import TranslationOptions, register

# @register
class GeoSpatialData(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    palika_name=models.CharField(max_length=100, blank=True, null=True)
    geom= gismd.GeometryField(srid=4326, null=True, blank=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    file_type=models.CharField(max_length=100, blank=True, null=True) 
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    data_file=models.FileField(upload_to= 'geospatialdata/', blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class PalikaUpload(models.Model):
    data_file=models.FileField(upload_to= 'geospatialdata/' ,blank=True, null=True)
    #data_file=models.FileField(models. FileField(upload_to='png_files/', validators=
#[FileExtensionValidator(allowed_extensions=['shp','shx','prj','dbf','cpg','geojson'])]))
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    
    
class PalikaGeometry(models.Model):
    palikaupload=models.ForeignKey(PalikaUpload, on_delete=models.CASCADE, blank=True, null=True)
    palika_name=models.CharField(max_length=100, blank=True, null=True)
    geom= gismd.GeometryField(srid=4326, null=True, blank=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    district= models.CharField(max_length=100, blank=True, null=True)
    state=models.CharField(max_length=100, blank=True, null=True)


# class GeoJsonData(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     username = models.CharField(max_length=100, blank=True, null=True)
#     palika_name=models.CharField(max_length=100, blank=True, null=True)
#     geom= gismd.GeometryField(srid=4326, null=True, blank=True)
#     description=models.TextField(max_length=1000, blank=True, null=True)
#     file_type=models.CharField(max_length=100, blank=True, null=True) 
#     upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
#     data_file=models.FileField(upload_to= 'GeoJsondata/', blank=True, null=True)

#     def __str__(self):
#         return self.username
    
# class JsonUpload(models.Model):
#     data_file=models.FileField(upload_to= 'GeoJosnData/' ,blank=True, null=True)
#     upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True) 


# class JsonGeometry(models.Model):
#     palikaupload=models.ForeignKey(PalikaUpload, on_delete=models.CASCADE, blank=True, null=True)
#     palika_name=models.CharField(max_length=100, blank=True, null=True)
#     geom= gismd.GeometryField(srid=4326, null=True, blank=True)
#     description=models.TextField(max_length=1000, blank=True, null=True)
#     upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
#     user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)       
