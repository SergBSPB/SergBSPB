# Generated by Django 4.1.7 on 2023-04-15 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0007_remove_observation_is_closed_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='observation',
            options={'ordering': ['-date_created'], 'verbose_name': 'Наблюдение по безопасности', 'verbose_name_plural': 'Наблюдения по безопасности'},
        ),
        migrations.AlterField(
            model_name='observation',
            name='character',
            field=models.CharField(choices=[('М-', 'Место(-)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Условия труда не безопасные'), ('М+', 'Место(+)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Условия труда безопасные'), ('П-', 'Поведение(-)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Поведение не безопасные'), ('П+', 'Поведение(+)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Поведение безопасные')], default='', max_length=35, verbose_name='Характер наблюдения'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='managers', to='observations.employee', verbose_name='Руководитель'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owners', to='observations.staffgroup', verbose_name='создатель наблюдения'),
        ),
    ]
