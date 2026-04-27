from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, When, F
import random
import datetime

from .models import Property
from .serializers import PropertyDetailSerializer, PropertyListSerializer


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 9
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
        month = self.request.query_params.get('month')  # Format: YYYY-MM
        term = self.request.query_params.get('term')    # 'short' or 'long'
        bedrooms = self.request.query_params.get('bedrooms')  # Number of bedrooms
        sort = self.request.query_params.get('sort')   # 'random', 'newest', 'price_asc', 'price_desc'

        # Apply city filter
        if city and city != 'All in Mauritius' and city != 'Any city in Mauritius':
            queryset = queryset.filter(city=city)

        # Apply bedrooms filter
        if bedrooms and bedrooms.isdigit():
            queryset = queryset.filter(bedrooms=int(bedrooms))

        # Apply term filter (short-term vs long-term based on actual fields)
        if term == 'long':
            # Long-term: properties with monthly rate > 0
            queryset = queryset.filter(rate_per_month__gt=0)
            price_field = 'rate_per_month'
        else:
            # Short-term (default): properties with daily rate > 0
            queryset = queryset.filter(rate_per_day__gt=0)
            price_field = 'rate_per_day'

        # Apply month availability filter
        if month:
            try:
                # Parse month (format: YYYY-MM)
                year, month_num = map(int, month.split('-'))
                start_date = datetime(year, month_num, 1).date()
                
                # Calculate end date (last day of month)
                if month_num == 12:
                    end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
                else:
                    end_date = datetime(year, month_num + 1, 1).date() - timedelta(days=1)
                
                # Filter properties that have at least one available day in the month
                # This excludes properties that are fully booked or fully blocked for the entire month
                
                # Get all property IDs that have at least one available date in the month
                available_property_ids = []
                
                for property_obj in queryset:
                    # Get booked dates for this property in the month range
                    booked_dates = Booking.objects.filter(
                        property=property_obj,
                        status__in=['confirmed', 'pending'],
                        check_in__lte=end_date,
                        check_out__gte=start_date
                    )
                    
                    # Get blocked dates for this property in the month range
                    blocked_dates = BlockedDate.objects.filter(
                        property=property_obj,
                        start_date__lte=end_date,
                        end_date__gte=start_date
                    )
                    
                    # Check if there's any availability in the month
                    # Generate all dates in the month
                    current_date = start_date
                    has_availability = False
                    
                    while current_date <= end_date:
                        # Check if date is booked or blocked
                        is_booked = booked_dates.filter(
                            check_in__lte=current_date,
                            check_out__gt=current_date
                        ).exists()
                        
                        is_blocked = blocked_dates.filter(
                            start_date__lte=current_date,
                            end_date__gte=current_date
                        ).exists()
                        
                        if not is_booked and not is_blocked:
                            has_availability = True
                            break
                        
                        current_date += timedelta(days=1)
                    
                    if has_availability:
                        available_property_ids.append(property_obj.id)
                
                # Filter queryset to only properties with availability
                queryset = queryset.filter(id__in=available_property_ids)
                
            except (ValueError, TypeError):
                # Invalid month format, skip filter
                pass

        # Apply sorting
        if sort == 'random':
            queryset = queryset.order_by('?')
        elif sort == 'newest':
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
        context['term'] = self.request.query_params.get('term', 'short')
        return context


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]
