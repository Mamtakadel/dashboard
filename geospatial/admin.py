

#admin
from django.contrib import admin
from todo.models import Todo


# Register your models here.

from django.contrib import admin

from geospatial.models import  PalikaUpload, PalikaGeometry, WeatherForecast

# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['id','user', 'title','description', 'is_completed','is_created','category']
#     list_filter= ("category", "is_completed") 
#     search_fields=['title']

class UserAuthAdmin(admin.ModelAdmin):
    list_display=['id', 'username', 'password']    

# class GeoSpatialDataAdmin(admin.ModelAdmin):
#     list_display=['user', 'username','geom', 'palika_name', 'description', 'file_type', 'upload_date', 'data_file']
    
class PalikaUploadAdmin(admin.ModelAdmin):
    list_display=['name','file','file_type','description','created_by' , 'uploaded_date']
    
class PalikaGeometryAdmin(admin.ModelAdmin):
    list_display=['palika','attr_data','bbox','area','district','ward_number']


class WeatherForecastAdmin(admin.ModelAdmin):
    list_display=['precipitation', 'temperature_2m', 'rain', 'date', 'relative_humidity_2m']    

# this is running--------------------------
           
    

# admin.site.register(GeoSpatialData, GeoSpatialDataAdmin)
admin.site.register(PalikaUpload, PalikaUploadAdmin)
admin.site.register(PalikaGeometry, PalikaGeometryAdmin)
admin.site.register(WeatherForecast, WeatherForecastAdmin)
# admin.site.register(GeoJsonData, GeoJsonDataAdmin)
# admin.site.register(JsonUpload, JsonUploadAdmin)
# admin.site.register(JsonGeometry, JsonGeometryAdmin)



    
#admin.site.site_header = "Todo List Panel"
