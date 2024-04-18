

from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from geospatial.views import UploadData , GetData, DownloadPalika, DownloadWard,check_status


router=DefaultRouter()
router.register(r'fileupload',UploadData)
router.register(r'getdata',GetData)
router.register(r'downloadpalika',DownloadPalika)
router.register(r'downloadward',DownloadWard)





# from django.urls import path, include
# from rest_framework.routers import  DefaultRouter
# from geospatial.views import Geom , GetJsonData, WardFilter 
# from geospatial.views import DownloadData

# router=DefaultRouter()
# router.register(r'Download',DownloadData)
# router.register(r'Fileupload', UploadData)
# router.register(r'GetJson',  GetJsonData)
# router.register(r'wardfilter',WardFilter)

# #router.register(r'GetJsonData',GetJsonData)
urlpatterns = [
    # path('', include(router.urls)),
    # path('postgeom/', Geom.a(), name='postgeom'),
    #path('palikageometry/', GetData.as_view(), name='palikageometry'),
    #path('check-status/', GetData.as_view(), name='palikageometry'),
    
    path('check_status/', check_status, name='check_status'),
]

urlpatterns += [
    path('', include(router.urls)),
]