# Generated by Django 2.1.1 on 2018-12-08 23:50

from django.db import migrations, models
import tenants_app.utils


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0003_auto_20181203_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paybox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_in_paybox', models.FloatField(default=0, max_length=45, verbose_name='Положили в кассу')),
                ('cash_taken', models.FloatField(default=0, max_length=45, verbose_name='Забрали из кассы')),
                ('cash_remain', models.FloatField(default=0, max_length=45, verbose_name='Денег в кассе')),
            ],
            options={
                'verbose_name': 'Paybox',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='rent_of_shelf',
            field=tenants_app.utils.CustomBooleanField(default=True, verbose_name='Плата за аренду полки'),
        ),
    ]