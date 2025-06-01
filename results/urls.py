from django.urls import path
from django.conf.urls.static import static
from results import views as result_views 
from django.contrib.auth import views as auth_views
from . import views
from .views import  ResultDetailView, ResultDetail2View, ResultDetail3View, ResultUpdateView, ResultUpdateView2, ResultUpdateView3
# from . import views

app_name = 'results'

urlpatterns = [
    path('print-result/', result_views.printresult, name="print-result"),
    path('print-second-result/', result_views.printresult2, name="print-second-result"),
    path('print-third-result/', result_views.printresult3, name="print-third-result"), 

    path('result-sheet/', result_views.resultsheet, name="result-sheet"),
    path('result-create/', result_views.result_create_form, name="result-create"),

    path('my-result/', result_views.view_self_result, name="my-result"),
    path('mysecond-term-result/', result_views.view_self_result2, name="mysecond-term-result"),
    path('mythird-term-result/', result_views.view_self_result3, name="mythird-term-result"),

    path('print-resultform/', result_views.printresultform, name="print-resultform"),
    path('upload-result/', result_views.uploadresult, name="upload-result"),
   
    path('my-reportsheet/', result_views.view_self_reportsheet, name="my-reportsheet"),

    # Results Update Views
    path('<int:id>/result-update/', ResultUpdateView.as_view(), name="result-update"),
    path('<int:id>/second-result-update/', ResultUpdateView2.as_view(), name="second-result-update"),
    path('<int:id>/third-result-update/', ResultUpdateView3.as_view(), name="third-result-update"),

    # # Results List Views
    # path('result-list/', ResultListView.as_view(), name='result-list'),
    # path('second-result-list/', ResultListView2.as_view(), name='second-result-list'),
    # path('third-result-list/', ResultListView3.as_view(), name='third-result-list'),

    # Results Detail Views
    path('<int:pk>/', ResultDetailView.as_view(), name='result-detail'), 
    path('<int:pk>/second-term/', ResultDetail2View.as_view(), name='second-term-detail'), 
    path('<int:pk>/third-term/', ResultDetail3View.as_view(), name='third-term-detail'), 

    # Results CSV FORMAT URLS
    path('result-csv', result_views.results_csv, name="result-csv"),
    path('second-result-csv', result_views.results_csv_2, name="second-result-csv"),
    path('third-result-csv', result_views.results_csv_3, name="third-result-csv"),
 
    # render resultsheet as pdf
    path('pdf/<pk>/', result_views.result_render_pdf_view, name="result-pdf-view"),
    path('pdf/<pk>/second-term/', result_views.result2_render_pdf_view, name="second-result-pdf-view"),
    path('pdf/<pk>/third-term/', result_views.result3_render_pdf_view, name="third-result-pdf-view"),
    #path('results/', PDFTemplateView.as_view(template_name='results/result_sheet.html',
    #                                       filename='my_result.pdf'), name='result-pdf'),

    #path to form-teachers class results
    path('my-student-results-first/', result_views.self_student_results_firsterm, name="my-students-results-first"),
    path('my-student-results-second/', result_views.self_student_results_secondterm, name="my-students-results-second"),
    path('my-student-results-third/', result_views.self_student_results_thirdterm, name="my-students-results-third"),


    
]
    # path('self-result/', views.SelfResultListView.as_view(), name='self-result'),
    