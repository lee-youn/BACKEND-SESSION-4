from django.db import models
from decimal import Decimal

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length= 256)
    description = models.CharField(max_length= 500)
    agree = models.IntegerField(default = 0)
    disagree = models.IntegerField(default = 0)
    agreeRate = models.DecimalField(max_digits=10,decimal_places=4, default=Decimal('0.0000'))
    disagreeRate = models.DecimalField(max_digits=10,decimal_places=4, default=Decimal('0.0000'))
    createdAt = models.DateTimeField(auto_now_add=True)

    # class Meta :
    #     db_table = 'poll'
