from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from payments.models import PaymentCategory, PaymentChart, PaymentDetail, BankDetail

# Register your models here.
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'description',)


class PaymentChartAdmin(admin.ModelAdmin):

    list_display=('name', 'payment_cat', 'amount_due', 'session',)
    list_filter  = ['payment_cat',]
    search_fields = ('session', 'term')
    exclude = ('term',)

class PaymentDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display=('student_detail', 'payment_name', 'amount_paid_a', 'payment_date_a', 'amount_paid_b', 'payment_date_b', 'amount_paid_c', 'payment_date_c', 'confirmed_a')
    list_filter  = ['student_detail__class_id']
    search_fields = ('student_detail__user__username', 'student_detail__last_name', 'student_detail__first_name')
    raw_id_fields = ['student_detail', 'payment_name']
    readonly_fields = ('no_of_payments',)
    # exclude = ('student_id',)


class BankDetailAdmin(admin.ModelAdmin):

    list_display=('bank_name', 'acc_name', 'acc_number',)




admin.site.register(PaymentCategory, PaymentCategoryAdmin)
admin.site.register(PaymentChart, PaymentChartAdmin)
admin.site.register(PaymentDetail, PaymentDetailAdmin)
admin.site.register(BankDetail, BankDetailAdmin)
