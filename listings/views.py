from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Property
from .serializers import PropertyDetailSerializer, PropertyListSerializer


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 100


class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all().order_by('order_number')
    serializer_class = PropertyListSerializer
    pagination_class = StandardPageNumberPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        availability = self.request.query_params.get('availability')
        period = self.request.query_params.get('period')

        if city and city != 'All in Mauritius':
            queryset = queryset.filter(city=city)

        if availability:
            queryset = queryset.filter(availabilities__month_year=availability)

        if period == 'Long-Term':
            queryset = queryset.filter(rate_per_month__gt=0)
        else:
            queryset = queryset.filter(rate_per_day__gt=0)

        return queryset.distinct().order_by('order_number')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['period'] = self.request.query_params.get('period', 'Short-Term')
        return context


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]
