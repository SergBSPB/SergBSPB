# Generated by Django 4.1.7 on 2023-03-27 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0005_alter_observation_site_alter_site_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managers', to='observations.employee', verbose_name='Руководитель'),
        ),
    ]