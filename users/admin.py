from django.contrib import admin
from users.models import Profile
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv, datetime


class UserProfileAdmin(admin.ModelAdmin):
           
    list_display=('user', 'code', 'user_type')
    list_filter  = ['user_type',]
    search_fields = ('user__username', 'code', 'user_type')


User = get_user_model()

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' 'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response

export_to_csv.short_description = 'Export to CSV'  #short description

# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''
    Registers the action in your model admin
    '''
    actions = [export_to_csv] 



# Register your models here.
admin.site.register(Profile, UserProfileAdmin)