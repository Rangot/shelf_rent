# Generated by Django 2.1.1 on 2018-11-15 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf_rent_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='name',
            field=models.CharField(default=1, max_length=45, verbose_name='ФИО'),
            preserve_default=False,
        ),
    ]
