

from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from geospatial.views import UploadData , GetData, DownloadPalika, DownloadWard,check_status ,WeatherApi


router=DefaultRouter()
router.register(r'fileupload',UploadData)
router.register(r'getdata',GetData)
router.register(r'downloadpalika',DownloadPalika)
router.register(r'downloadward',DownloadWard)








# #router.register(r'GetJsonData',GetJsonData)
urlpatterns = [
    # path('', include(router.urls)),
    # path('postgeom/', Geom.a(), name='postgeom'),
    #path('palikageometry/', GetData.as_view(), name='palikageometry'),
    #path('check-status/', GetData.as_view(), name='palikageometry'),
    
    path('check_status/', check_status, name='check_status'),
    path('weatherapi/', WeatherApi.as_view(), name='weatherapi'),
]

urlpatterns += [
    path('', include(router.urls)),
]