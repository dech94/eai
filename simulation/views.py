from django.shortcuts import render
from django.views.generic import TemplateView

class ConnectionInfoView(TemplateView):
    template_name = 'simulation/connection_info.html'
