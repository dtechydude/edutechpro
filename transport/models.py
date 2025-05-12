from django.db import models
from students.models import Student
from staff.models import Staff
from django.template.defaultfilters import slugify
from django.urls import reverse
from curriculum.models import Session
from payments.models import BankDetail

# Create your models here.


class Route(models.Model):
    name = models.CharField(max_length=200, blank=True )
    direction = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')
    staff_in_charge = models.ForeignKey(Staff, on_delete=models.CASCADE, default=None, null=True)
    slug = models.SlugField(null=True, blank=True)


    def __str__ (self):
        return f'{self.name} {self.staff_in_charge} '

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BusFee(models.Model):
    amount = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default= None, related_name='route_name')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default= None, related_name='route_name')
    term = models.ForeignKey(Route, on_delete=models.CASCADE, default= None, related_name='route_name')

    class Meta:
        ordering = ['-amount' ]        

    def __str__ (self):
       return f'{self.amount} {self.term} '

    # def get_absolute_url(self):
    #     return reverse('payment:my_payments')  
    

class StudentBusPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default= None, related_name='route_name')
    payment = models.ForeignKey(BusFee, on_delete=models.CASCADE, default= None, related_name='route_name')

    amount_paid_a = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='First Payment Amount')
    bank_name_a = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True, related_name='bank_name_a')   
    payment_date_a = models.DateField()
    remark_a = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')

    amount_paid_b = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='Second Payment Amount')
    bank_name_b = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='bank_name_b')   
    payment_date_b = models.DateField(blank=True, null=True)
    remark_b = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')

    amount_paid_c = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, help_text='Third Payment Amount')
    bank_name_c = models.ForeignKey(BankDetail, on_delete=models.CASCADE, default=None, null=True, blank=True)   
    payment_date_c = models.DateField(blank=True, null=True)
    remark_c = models.CharField(max_length=200, blank=True, verbose_name='description(if any)')

    discount = models.DecimalField(help_text='enter in (%) leave empty if no discoun is given', max_digits=3, decimal_places=0, blank=True, null=True, verbose_name='TOTAL DISCOUNT(if any)', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    # payment confirmation
    confirmed_a = models.BooleanField(default=False) 
    confirmed_b = models.BooleanField(default=False) 
    confirmed_c = models.BooleanField(default=False) 

    payment_updated_date = models.DateField(auto_now_add=True)     

    class Meta:
        ordering = ['-student' ]

        unique_together = ['student', 'payment_name']
    

    def __str__ (self):
       return f'{self.student} {self.student} '

    def get_absolute_url(self):
        return reverse('payment:my_payments')  
    
    # def get_absolute_url(self):
    #     return reverse('payment:payment_detail', kwargs={'id':self.id})
    