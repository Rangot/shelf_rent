# Generated by Django 2.1.1 on 2018-09-20 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0040_auto_20180920_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='all_payment',
            field=models.CharField(blank=True, default=None, max_length=45, null=True),
        ),
    ]