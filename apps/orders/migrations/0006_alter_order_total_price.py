# Generated by Django 4.1.1 on 2022-09-14 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_coupon_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='총 주문금액'),
        ),
    ]
