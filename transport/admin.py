from django.contrib import admin
from .models import Route, BusFee, StudentBusPayment
from import_export.admin import ImportExportModelAdmin



class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'route_id', 'direction', 'staff_in_charge', 'driver')
    search_fields = ('name', 'staff_in_charge__full_name',)
    ordering = ['name',]
    exclude = ('slug',)

class BusFeeAdmin(admin.ModelAdmin):
    list_display = ('route', 'amount_due', 'session', 'term')
    search_fields = ('route', 'amount_due', 'session', 'term')
    ordering = ['route',]


class StudentBusPaymentAdmin(admin.ModelAdmin):
    list_display = ('payee_id', 'route', 'payment', 'amount_paid_a', 'confirmed_a')
    search_fields = ('route', 'payment')
    ordering = ['route',]





admin.site.register(Route, RouteAdmin)
admin.site.register(BusFee, BusFeeAdmin)
admin.site.register(StudentBusPayment, StudentBusPaymentAdmin)

