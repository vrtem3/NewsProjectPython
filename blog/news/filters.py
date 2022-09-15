from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    dateCreate = DateFilter(field_name='dateCreate',
                      lookup_expr='gte',
                      label='Создан позднее',
                      widget=DateTimeInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'dateCreate', 'categoryType']

