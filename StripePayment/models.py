from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=300, verbose_name="Имя")
    description = models.CharField(max_length=2000, verbose_name="Описание")
    price = models.IntegerField(default=0, verbose_name="Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Заказы")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"