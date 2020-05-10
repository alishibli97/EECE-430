import django_filters
from django_filters import DateFilter,CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="order_datetime",lookup_expr="gte")
    end_date = DateFilter(field_name="order_datetime",lookup_expr="lte")
    note = CharFilter(field_name='order_note',lookup_expr='icontains')

    
    class Meta:
        model=Order
        fields = "__all__"
        exclude = ['order_customer','order_datetime','order_note']
