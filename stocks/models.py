from django.db import models

from users.models import NormalUser


# Create your models here.

class Trades(models.Model):
    stock = models.CharField(max_length=8, null=False)
    is_buy = models.BooleanField(null=False)

    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name="+")
    time_added = models.DateTimeField("Time added", auto_now_add=True)


    def is_buy_string(self):
        return "Buy" if self.is_buy else "Sell"