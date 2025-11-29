from django.contrib import admin
from django.urls import path
from simulation.views import ConnectionInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ConnectionInfoView.as_view(), name='connection_info'),
]
