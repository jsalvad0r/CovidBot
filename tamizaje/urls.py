from django.contrib import admin
from django.urls import path, include
from tamizaje.views import PatientView, webhook

app_name = 'tamizaje'

urlpatterns = [
    path('', PatientView.as_view(), name='index'),
    path('webhook/', webhook, name='webhook'),
    path('api/', include('tamizaje.api.urls', namespace='api'))
]