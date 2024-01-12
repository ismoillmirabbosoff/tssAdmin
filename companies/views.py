from django.shortcuts import render

# Create your views here.
# from django.shortcuts import get_object_or_404
from .models import Device, Company
from django.views import generic

class DeviceDetailView(generic.DetailView):
    model = Device
    
    slug_url_kwarg = 'qrID'
    slug_field = 'qrID'

    # model = Company.objects.get(pk=model.companyId)
