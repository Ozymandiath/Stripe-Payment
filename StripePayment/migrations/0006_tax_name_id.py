# Generated by Django 4.1.6 on 2023-02-13 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StripePayment', '0005_tax_order_taxs'),
    ]

    operations = [
        migrations.AddField(
            model_name='tax',
            name='name_id',
            field=models.CharField(default=0, max_length=15, verbose_name='ID комиссии'),
            preserve_default=False,
        ),
    ]
