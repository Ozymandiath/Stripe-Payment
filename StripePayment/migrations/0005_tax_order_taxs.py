# Generated by Django 4.1.6 on 2023-02-13 08:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StripePayment', '0004_discount_name_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Название комиссии')),
                ('percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Процент комиссии')),
                ('inclusive', models.BooleanField(verbose_name='Входит в стоимость?')),
            ],
            options={
                'verbose_name': 'Налог',
                'verbose_name_plural': 'Комиссии',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='taxs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StripePayment.tax', verbose_name='Налог'),
        ),
    ]
