# Generated by Django 2.0.6 on 2018-08-22 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0026_auto_20180822_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='shelf',
            field=models.OneToOneField(db_column='shelf', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tenants_app.Shelf', verbose_name='Полка'),
        ),
    ]
