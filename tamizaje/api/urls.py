from django.urls import path
from .views import PatientListAPIView

app_name = 'tamizaje:api'

urlpatterns = [
    path('patients/', PatientListAPIView.as_view(), name='patients')
]