from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=2000)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

