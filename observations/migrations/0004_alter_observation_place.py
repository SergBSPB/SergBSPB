# Generated by Django 4.1.7 on 2023-03-27 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0003_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='places', to='observations.place', verbose_name='Место наблюдения'),
        ),
    ]
