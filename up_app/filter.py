import  django_filters
from .models import *

class ProductFilter(django_filters.filterset):
    class Meta:
        model = Product
        filter = '__all__'


