from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_item(value):
    c = 1
    c = value
    return value


class Currency(models.Model):
    US = "USD"
    Russia = "RUB"
    currency_choices = [
        (US, "United States"),
        (Russia, "Russia"),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices, verbose_name="Страна")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return self.currency


class Item(models.Model):
    name = models.CharField(max_length=300, verbose_name="Имя")
    description = models.CharField(max_length=2000, verbose_name="Описание")
    price = models.IntegerField(default=0, verbose_name="Цена")
    currency = models.ForeignKey("Currency", on_delete=models.CASCADE, verbose_name="Валюта", default=1)

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"

    def __str__(self):
        return self.name


class Order(models.Model):
    promo = models.ForeignKey("Discount", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Промокод")
    taxs = models.ForeignKey("Tax", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Налог")
    item = models.ManyToManyField("Item", validators=[validate_item], verbose_name="Заказы")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.id)

    def count_item_ir_order(self):
        return str(self.item.count())


class Discount(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название промокода")
    name_id = models.CharField(max_length=15, verbose_name="ID промокода")
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                  verbose_name="Процент скидки")
    currency = models.ForeignKey("Currency", on_delete=models.CASCADE, verbose_name="Валюта")

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=10, verbose_name="Название комиссии")
    name_id = models.CharField(max_length=15, verbose_name="ID комиссии")
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                  verbose_name="Процент комиссии")
    inclusive = models.BooleanField(verbose_name="Входит в стоимость?")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Комиссии"

    def __str__(self):
        return self.name
