
from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from geospatial.views import Geom, GeoSpatial,GetData


router=DefaultRouter()
router.register(r'geo', GeoSpatial)
urlpatterns = [
    path('', include(router.urls)),
    path('postgeom/', Geom.as_view(), name='postgeom'),
    path('palikageometry/', GetData.as_view(), name='palikageometry'),
    
]