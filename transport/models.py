from django.db import models
from students.models import Student
from staff.models import Staff
from django.template.defaultfilters import slugify
from django.conf import settings
from django.urls import reverse
from curriculum.models import Session
from payments.models import BankDetail
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator 


# Create your models here.


class Route(models.Model):
    route_id = models.CharField(max_length=8,null=True, blank=True, help_text='Could be Bus Number')
    name = models.CharField(max_length=200, blank=True )
    direction = models.CharField(max_length=200, blank=True)
    staff_in_charge = models.ForeignKey(Staff, on_delete=models.CASCADE, default=None, null=True, related_name='official_staff')
    driver = models.ForeignKey(Staff, on_delete=models.CASCADE, default=None, null=True, related_name='bus_driver')
    slug = models.SlugField(null=True, blank=True)

    def __str__ (self):
        return f'{self.name} - {self.route_id}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BusFee(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default= None, related_name='route_name')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default= None, related_name='academic_session')
    term = models.ForeignKey(Session, on_delete=models.CASCADE, default= None, related_name='term_name')
    amount_due = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='Bus Fare', verbose_name='Bus Fare')

    class Meta:
        ordering = ['-amount_due' ]        

    def __str__ (self):
       return f'{self.amount_due} - {self.route.name} - {self.route.route_id}'

    # def get_absolute_url(self):
    #     return reverse('payment:my_payments')  
    

class StudentBusPayment(models.Model):
    payee_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True,  help_text='confirmusername', related_name='student_id')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default= None, related_name='routes')
    payment = models.ForeignKey(BusFee, on_delete=models.CASCADE, default= None, related_name='payments')

    amount_paid_a = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='First Payment')
    bank_name_a = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True, related_name='bank_name_a')   
    payment_date_a = models.DateField()
    remark_a = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')

    amount_paid_b = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='Second Payment')
    bank_name_b = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='bank_name_b')   
    payment_date_b = models.DateField(blank=True, null=True)
    remark_b = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')

    amount_paid_c = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='Third Payment Amount')
    bank_name_c = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True, blank=True)   
    payment_date_c = models.DateField(blank=True, null=True)
    remark_c = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')

    discount = models.DecimalField(help_text='enter in (%) leave empty if no discoun is given', max_digits=3, decimal_places=0, blank=True, null=True, verbose_name='TOTAL DISCOUNT(if any)', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    # payment confirmation
    confirmed_a = models.BooleanField(default=False, verbose_name='Confirmed_1') 
    confirmed_b = models.BooleanField(default=False, verbose_name='Confirmed_3') 
    confirmed_c = models.BooleanField(default=False, verbose_name='Confirmed_3') 

    payment_updated_date = models.DateField(auto_now_add=True)     

    class Meta:
        ordering = ['-payee_id' ]

        unique_together = ['payee_id', 'route']
    

    def __str__ (self):
       return f'{self.payee_id} {self.payee_id} '

    @property
    def balance_pay(self):
       return self.payment_name.amount_due - (self.amount_paid_a + self.amount_paid_b + self.amount_paid_c)
    
    @property
    def total_amount_paid(self):
       return (self.amount_paid_a + self.amount_paid_b + self.amount_paid_c)
    