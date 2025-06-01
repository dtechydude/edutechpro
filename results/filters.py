import django_filters
from .models import UploadCertificate, ResultSheet1, ResultSheet2, ResultSheet3
from django.contrib.auth.models import User

class MyresultFilter(django_filters.FilterSet):

    class Meta:
        model = UploadCertificate
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam', 'session',}
        

class MyResultSheetFilter(django_filters.FilterSet):

    class Meta:
        model = ResultSheet1
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam__name', 'exam__session',}
        

class ResultSheetFilter(django_filters.FilterSet):

    class Meta:
        model = ResultSheet1
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam__session', 'exam__standard',}


class ResultSheetFilter2(django_filters.FilterSet):

    class Meta:
        model = ResultSheet2
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam__session', 'exam__standard',}


class ResultSheetFilter3(django_filters.FilterSet):

    class Meta:
        model = ResultSheet3
        # # fields = '__all__'
        # fields = {'current_class': ['exact']}
        fields = {'exam__session', 'exam__standard',}
        