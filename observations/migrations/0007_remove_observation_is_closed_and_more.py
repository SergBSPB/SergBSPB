# Generated by Django 4.1.7 on 2023-04-01 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0006_alter_observation_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observation',
            name='is_closed',
        ),
        migrations.AlterField(
            model_name='observation',
            name='character',
            field=models.CharField(choices=[('М-', 'Место(-)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Условия труда не безопасные'), ('М+', 'Место(+)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Условия труда безопасные'), ('П-', 'Поведение(-)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Поведение не безопасные'), ('П+', 'Поведение(+)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Поведение безопасные')], default='', max_length=35, verbose_name='Характер наблюдения'),
        ),
    ]
