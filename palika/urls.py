from django.urls import path, include

from palika.views import SignUpApiView

urlpatterns = [
    path('signup/', SignUpApiView.as_view(), name='signup'),
]