from rest_framework.generics import ListAPIView
from tamizaje.models import Patient
from .serializers import PatientSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 3
    def get_paginated_response(self, data):
        #import pdb; pdb.set_trace()
        return Response({
            'total': self.page.paginator.count,
            'per_page': self.page_size,
            'current_page': self.page.number,
            'last_page': self.page.paginator.num_pages,
            'next_page_url': self.get_next_link(),
            'prev_page_url': self.get_previous_link(),
            'from': (self.page_size * self.page.number - 5) + 1,
            'to': self.page_size * self.page.number,
            'data': data
        })


class PatientListAPIView(ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = CustomPagination