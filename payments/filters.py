import django_filters
from .models import PaymentChart, PaymentDetail1
from django.contrib.auth.models import User

class PaymentFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail1
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payment_name',}

class MyPaymentFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail1
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payment_name'}

class PaymentChartFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentChart
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'session', 'payment_cat', 'term',}


class PaymentReportFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail1
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payee' }

class PaymentSummaryFilter(django_filters.FilterSet):

    class Meta:
        model = PaymentDetail1
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'payee', }
        

