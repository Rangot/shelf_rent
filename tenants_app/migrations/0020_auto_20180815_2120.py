# Generated by Django 2.0.6 on 2018-08-15 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenants_app', '0019_auto_20180815_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='rents',
            field=models.ForeignKey(blank=True, db_column='rents', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tenants_app.Rents', verbose_name='Договор'),
        ),
    ]
