# Generated by Django 2.0.6 on 2018-08-09 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0015_auto_20180809_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rents',
            name='number',
            field=models.CharField(blank=True, max_length=45, null=True, unique=True),
        ),
    ]
