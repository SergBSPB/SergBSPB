# Generated by Django 4.1.7 on 2023-04-16 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0009_alter_observation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='manager',
            field=models.ForeignKey(blank=True, default=8, on_delete=django.db.models.deletion.PROTECT, related_name='managers', to='observations.employee', verbose_name='Руководитель'),
            preserve_default=False,
        ),
    ]
