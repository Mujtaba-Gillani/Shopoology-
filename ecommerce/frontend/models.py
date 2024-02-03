from django.db import models

# Create your models here.
class Cake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=[('Birthday', 'Birthday'), ('Wedding', 'Wedding'), ('Custom', 'Custom')])
    image = models.ImageField(upload_to='cakes/')
    active = models.BooleanField(default=True)
