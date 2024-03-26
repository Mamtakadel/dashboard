# #Class Based view
from django.urls import path, include

from .views import (
    TodoApiView,
)



# # Model Based View
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from todo.views import TaskViewSet

# router = DefaultRouter()
# router.register(r'demo', TaskViewSet)

# urlpatterns = [
#     path('modelviewset', include(router.urls)),
# ]


urlpatterns = [
    path('api/', TodoApiView.as_view()),
    
    
]


# Functional View sets