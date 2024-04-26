
from django.db import models

from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismd
from django.core.validators import FileExtensionValidator
# from modeltranslation.translator import TranslationOptions, register

# @register
# class GeoSpatialData(models.Model):
#     # username = models.CharField(max_length=100, blank=True, null=True)
#     geom= gismd.GeometryField(srid=4326, null=True, blank=True)
#     attr_data=models.JSONField(blank=True, null=True)
#     palika= models.ForeignKey()
    # data_file=models.FileField(upload_to= 'geospatialdata/', blank=True, null=True)
    # upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    
    # def __str__(self):
    #     return self.username
    
class PalikaUpload(models.Model):
    name=models.CharField(max_length=100, blank=True, null=True)
    file=models.FileField(upload_to= 'geospatialdata/' ,blank=True, null=True)
    file_type=models.CharField(max_length=100, blank=True, null=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    uploaded_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    
    
class PalikaGeometry(models.Model):
    palika=models.ForeignKey(PalikaUpload, on_delete=models.CASCADE, blank=True, null=True)
    geom= gismd.GeometryField(srid=4326, null=True, blank=True)
    attr_data=models.JSONField(blank=True, null=True)
    bbox=models.CharField(max_length=100,blank=True,null=True)
    area= models.FloatField(blank=True,null=True)
    district= models.CharField(max_length=100, blank=True, null=True)
    #state=models.CharField(max_length=100, blank=True, null=True)
    ward_number =models.CharField(max_length=100,blank=True,null=True)


################################      Weather API ################################################    
class WeatherForecast(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    date=models.DateTimeField(blank=True, null=True)
    temperature_2m=models.FloatField(blank=True, null=True)
    relative_humidity_2m=models.FloatField(blank=True, null=True)
    precipitation=models.FloatField(blank=True, null=True)
    rain=models.FloatField(blank=True, null=True)


    
