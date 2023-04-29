from datetime import timedelta, datetime

import django_filters
from django import forms

from .models import *
one_month_ago = date.today() - timedelta(days=30)

class ObservationsFilter(django_filters.FilterSet):

    date_created_gte = django_filters.DateFilter(label='От', field_name='date_created', lookup_expr='gte',
                                      widget=forms.DateInput(attrs={'type': 'date',
                                                                    'value': one_month_ago }))
    date_created_lte = django_filters.DateFilter(label='До', field_name='date_created', lookup_expr='lte',
                                    widget=forms.DateInput(attrs={'type': 'date', 'value': date.today, }))


    class Meta:
        model = Observation
        fields = ['date_created_gte', 'date_created_lte']

        # fields = ['owner', 'users_organization', 'users_department', 'character', 'dialog', 'risk', 'view', 'site',
        #           'category', 'control', 'manager', 'status', 'date_created_gte', 'date_created_lte']
