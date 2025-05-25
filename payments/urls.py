from django.urls import path
from payments import views as payment_views
from payments.views import PaymentCreateView
from . import views



app_name = 'payments'

urlpatterns = [
    path('payment-form/', payment_views.payment_form, name="payment_form"),
    path('payment-instruction/', payment_views.payment_instruction, name="payment_instruction"),      
    path('payment-report/', payment_views.payment_report, name="payment_report"),
    # path('summary-payment-report/', payment_views.summary_payment_report, name="summary_payment_report"),
    path('debtor-list/', payment_views.debtor_list, name="debtor_list"),      
    path('payment-cat-form/', payment_views.payment_cat_form, name="payment_cat_form"),
    path('payment-chart-form/', payment_views.payment_chart_form, name="payment_chart_form"),
    path('payment-summary/', payment_views.paymentlist, name="payment_summary"),
    path('payment-chart/', payment_views.payment_chart_list, name="payment_chart"),
    path('my-payments/', payment_views.view_self_payments, name="my_payments"),
    # path('mypayment/', views.MypaymentListView.as_view(), name='mypayment_list'),
    # path('make-payment/', payment_views.make_payments, name="make_payment"),
    path('payment-pdf', payment_views.allpayment_pdf, name="payment-pdf"),
    path('payment-csv', payment_views.allpayment_csv, name="payment-csv"),
    path('debtor-csv', payment_views.debtor_csv, name="debtor-csv"),
    path('payment_chart-pdf', payment_views.payment_chart_pdf, name="payment_chart-pdf"),
    path('payment_chart-csv', payment_views.payment_chart_csv, name="payment_chart-csv"),

    path('payment-create/', views.PaymentCreateView.as_view(), name="payment-create"),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payment-category/', views.PaymentCategoryListView.as_view(), name='payment-category'),
    path('bank-list/', views.BankListView.as_view(), name='bank-list'),
    path('bank-create/', views.BankCreateView.as_view(), name="bank-create"),
       
    path('<int:pk>/payment_update', views.PaymentUpdateView.as_view(), name='payment_update'),

    # Search student detail app
    path('payment-search/', payment_views.payment_search_list, name='payment_search_list'),
    path('search/', payment_views.search, name='search'),

    # render receipt as pdf
    path('pdf/<pk>/', payment_views.receipt_render_pdf_view, name="receipt-pdf-view"),
]
