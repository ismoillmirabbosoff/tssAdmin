from django.urls import path
from .views import DeviceDetailView

urlpatterns = [

    path('devices/<slug:qrID>', DeviceDetailView.as_view(),name="device-details"),
]