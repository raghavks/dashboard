from rest_framework.decorators import api_view
from rest_framework.response import Response
from Ele_CC_Raghavendra import settings
from django.shortcuts import render
import Ele_CC_Raghavendra.dashboard_stufs.dashboard as dashboard


@api_view(['GET'])
def render_dashboard(request):
    return render(request, 'dashboard.html', {'STATIC_URL': settings.STATIC_URL})


@api_view(['GET'])
def render_index_file(request):
    return render(request, 'index.html', {'STATIC_URL': settings.STATIC_URL})


@api_view(['GET'])
def perform_computation(request):
    return Response({"request": dashboard.service_sms_type()})
