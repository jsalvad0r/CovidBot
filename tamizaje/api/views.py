from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from tamizaje.models import Patient

from .serializers import PatientSerializer


class CustomPagination(PageNumberPagination):
    page_size = 20
    def get_paginated_response(self, data):
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
    serializer_class = PatientSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        params = self.request.query_params
        queryset = Patient.objects.all()
        if 'death_rate_covid19' in params:
            if params.get('death_rate_covid19') == 'bajo':
                queryset = queryset.filter(death_rate_covid19__lt=50.00)
            elif params.get('death_rate_covid19') == 'intermedio':
                queryset = queryset.filter(death_rate_covid19__gte=50.00, death_rate_covid19__lt=80.00)
            elif params.get('death_rate_covid19') == 'alto':
                queryset = queryset.filter(death_rate_covid19__gte=80.00)
        return queryset.order_by('-death_rate_covid19')
