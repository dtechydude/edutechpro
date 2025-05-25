from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentDetail


@receiver(post_save, sender=PaymentDetail)
def post_save_create_trans_id(sender, instance, created, *args, **kwargs):
    if created:
        PaymentDetail.objects.create(student_detail=instance)

@receiver(post_save, sender=PaymentDetail)
def save_paymentdetail(sender, instance, **kwargs):
    instance.paymentdetail.save()