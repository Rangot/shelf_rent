# Generated by Django 2.1.1 on 2018-09-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0037_auto_20180920_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='all_payment',
            field=models.CharField(default=0, max_length=45),
        ),
    ]