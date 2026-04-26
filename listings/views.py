from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, When, F
import random

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
        
        # Filtering parameters
        city = self.request.query_params.get('city')
        availability = self.request.query_params.get('availability')
        period = self.request.query_params.get('period')
        sort = self.request.query_params.get('sort')  # 'random', 'newest', 'price_asc', 'price_desc'

        # Apply city filter
        if city and city != 'All in Mauritius':
            queryset = queryset.filter(city=city)

        # Apply availability filter (you need to adjust to your actual availability logic)
        if availability:
            queryset = queryset.filter(availabilities__month_year=availability)

        # Apply period filter (short-term vs long-term)
        if period == 'Long-Term':
            queryset = queryset.filter(rate_per_month__gt=0)
            price_field = 'rate_per_month'
        else:
            queryset = queryset.filter(rate_per_day__gt=0)
            price_field = 'rate_per_day'

        # Apply sorting
        if sort == 'random':
            # Note: order_by('?') can be slow on large tables; consider alternatives if needed
            queryset = queryset.order_by('?')
        elif sort == 'newest':
            # Assumes higher id = newer (since no created_at field)
            queryset = queryset.order_by('-id')
        elif sort == 'price_asc':
            queryset = queryset.order_by(price_field)
        elif sort == 'price_desc':
            queryset = queryset.order_by(f'-{price_field}')
        else:
            # Default sorting (by order_number)
            queryset = queryset.order_by('order_number')

        return queryset.distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['period'] = self.request.query_params.get('period', 'Short-Term')
        return context


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]
