from django.urls import path
from transport import views as payment_views
from . import views


app_name = 'transport'

urlpatterns = [
    path('bus-payment-list/', payment_views.bus_paymentlist, name="bus_payment_list"),
    path('my-bus-payment/', payment_views.view_self_bus_payments, name="my_bus_payment"),      
    path('bus_payment_chart/', payment_views.bus_payment_chart, name="bus_payment_chart"),

]