from doctest import Example
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from results.models import Examination, UploadCertificate, MarkedSheet, Session, ResultSheet1, ExamSubject, MotorAbility1, ResultImage1, ResultSheet3, ExamSubject, MotorAbility3, ResultImage3, MotorAbility2, ResultImage2, ResultSheet2

# Register your models here.

class UploadCertificateAdmin(admin.ModelAdmin):
       
    list_display=('student', 'exam', 'session', 'file',)
    list_filter  = ['exam', 'exam']
    search_fields = ('student__user__username', 'student__last_name', 'student__first_name')
    raw_id_fields = ['student', 'standard', 'exam', 'session']

class ExamSubjectAdmin(admin.ModelAdmin):
       
    list_display=('subject_id', 'name',)
    exclude =['slug']

class MotorAbility1Inline(admin.TabularInline):
    model = MotorAbility1
    max_num = 1
    
    def has_delete_permission(self, request, obj=None):
        return False

class ResultImage1Inline(admin.TabularInline):
    model = ResultImage1
    exclude =['f_1', 'f_2', 'f_3']
    max_num = 1
    
    def has_delete_permission(self, request, obj=None):
        return False

class ResultSheet1Admin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [MotorAbility1Inline, ResultImage1Inline] 
    exclude =['remark', 'student_id']
    list_display=('student_detail', 'exam',)
    list_filter  = ['student_detail__standard']
    search_fields = ('student_detail__student_username', 'student_detail__full_name')
    raw_id_fields = ['student_id', 'student_detail',]

# Second Term Result
class MotorAbility2Inline(admin.TabularInline):
    model = MotorAbility2
    max_num = 1
    
    def has_delete_permission(self, request, obj=None):
        return False

class ResultImage2Inline(admin.TabularInline):
    model = ResultImage2
    exclude =['f_1', 'f_2', 'f_3']
    max_num = 1
    
    def has_delete_permission(self, request, obj=None):
        return False

class ResultSheet2Admin(admin.ModelAdmin):
    inlines = [MotorAbility2Inline, ResultImage2Inline] 
    exclude =['remark', 'standard']
    list_display=('student_detail', 'exam',)
    list_filter  = ['student_detail__standard']
    search_fields = ('student_detail__student_username', 'student_detail__first_name')
    raw_id_fields = ['student_id', 'student_detail']



# Third Term REsult
class MotorAbility3Inline(admin.TabularInline):
    model = MotorAbility3
    max_num = 1
    
    def has_delete_permission(self, request, obj=None):
        return False

class ResultImage3Inline(admin.TabularInline):
    model = ResultImage3
    exclude =['f_1', 'f_2', 'f_3']
    max_num = 1
    
    def has_delete_permission(self, request, obj=None):
        return False
    

class ResultSheet3Admin(admin.ModelAdmin):
    inlines = [MotorAbility3Inline, ResultImage3Inline] 
    exclude =['remark', 'student_id']
    list_display=('student_detail', 'exam',)
    list_filter  = ['student_detail__standard']
    search_fields = ('student_detail__student_username', 'student_detail__first_name')
    raw_id_fields = ['student_id', 'student_detail', 'first_term', 'second_term']


class ExaminationAdmin(admin.ModelAdmin):
       
    list_display=('name', 'standard', 'session')

class MarkedSheetAdmin(admin.ModelAdmin):
       
    list_display=('student', 'session', 'exam',)
    list_filter  = ['session', 'exam']
    search_fields = ('student__user__username', 'student__last_name', 'student__first_name')
    raw_id_fields = ['student', 'standard', 'exam', 'session', 'subject_name']

# class ResultImageAdmin(admin.ModelAdmin):
       
#     list_display= ['logo']
    
#     raw_id_fields = ['resultsheet']


# admin.site.register(MarkedSheet, MarkedSheetAdmin)
admin.site.register(Examination, ExaminationAdmin)
# admin.site.register(UploadCertificate, UploadCertificateAdmin)
admin.site.register(ExamSubject, ExamSubjectAdmin)
admin.site.register(ResultSheet1, ResultSheet1Admin)
admin.site.register(ResultSheet2, ResultSheet2Admin)
admin.site.register(ResultSheet3, ResultSheet3Admin)
# admin.site.register(ResultImage, ResultImageAdmin)
