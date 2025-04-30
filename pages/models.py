from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    alias = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__ (self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)