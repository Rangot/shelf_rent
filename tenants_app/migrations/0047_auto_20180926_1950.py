# Generated by Django 2.1.1 on 2018-09-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0046_remove_cash_take'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='discount',
            field=models.CharField(default=0, max_length=45, verbose_name='Скидка'),
        ),
    ]
