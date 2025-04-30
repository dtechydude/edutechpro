from django.db import models

# Create your models here.

class InventoryItems(models.Model):
    name = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)
    item_location = models.CharField(max_length=150, blank=True)
    quantity = models.IntegerField(default=1)
    # staff_in_charge = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, blank=True, null=True )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


    def __str__ (self):    
        return f'{self.name}'

    class Meta:
        verbose_name = 'Inventory Items'
        verbose_name_plural = 'Inventory Items'