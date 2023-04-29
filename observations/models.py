from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import safestring


placemin = safestring.mark_safe("Место(-)" + "&nbsp;"*17 + "Условия труда не безопасные")
placeplus = safestring.mark_safe("Место(+)" + "&nbsp;"*16 + "Условия труда безопасные")
behaviourmin = safestring.mark_safe("Поведение(-)" + "&nbsp;"*9 + "Поведение не безопасное")
behaviourplus = safestring.mark_safe("Поведение(+)" + "&nbsp;"*8 + "Поведение безопасное")

class StaffGroup(User):
    class Meta:
        proxy = True

    def __str__(self):
        fio = self.last_name + ' ' + self.first_name
        return str(fio)


class Organization(models.Model):
    name = models.TextField("Организация", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Department(models.Model):
    name = models.TextField("Ваш участок", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ваш участок'
        verbose_name_plural = 'Ваши участки'
        ordering = ['name']


class Employee(models.Model):
    user = models.OneToOneField(StaffGroup, on_delete=models.PROTECT,
                                verbose_name='Имя сотрудника', related_name='employee')
    users_organization = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Организация')
    users_department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Ваш участок')
    responsible_manager = models.ForeignKey(StaffGroup, on_delete=models.PROTECT,
                                            verbose_name='Ответственный руководитель', related_name='manager')
    is_manager = models.BooleanField(verbose_name="Является руководителем(да/нет)", default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['user']


class Category(models.Model):
    name = models.TextField("Категория", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class View(models.Model):
    name = models.TextField("Вид", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'


class Site(models.Model):
    name = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name="Участок из ваш участок")
    sites_organisation = models.ForeignKey(Organization, on_delete=models.PROTECT, verbose_name='Организация')
    sites_manager = models.ForeignKey(StaffGroup, on_delete=models.PROTECT, verbose_name='Руководитель участка')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Участок наблюдения'
        verbose_name_plural = 'Участки наблюдения'
        ordering = ['name']

class Place(models.Model):
    name = models.TextField("Место наблюдения", max_length=50)
    place_organisation = models.ForeignKey(Organization, on_delete=models.PROTECT,
                                           verbose_name='Организация')
    site_place = models.ForeignKey(Site, on_delete=models.PROTECT,
                                   verbose_name='Участок наблюдения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Место наблюдения'
        verbose_name_plural = 'Места наблюдения'
        ordering = ['name']


class Control(models.Model):
    name = models.TextField("Конторль", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контроль'
        verbose_name_plural = 'Контроль'


class Observation(models.Model):
    """ Наблюдения """

    STATUS_COMPLETED = 'Completed'
    STATUS_REJECTED = 'Rejected'
    STATUS_POSTPONED = 'Postponed'
    STATUS_PROGRESS = 'Progress'
    STATUS_NEW = 'New'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новое'),
        (STATUS_PROGRESS, 'В работе'),
        (STATUS_POSTPONED, 'Отложено'),
        (STATUS_REJECTED, 'Отклонено'),
        (STATUS_COMPLETED, 'Выполнено'),
    ]

    CHARACTER_CHOICES = (
        ('М-', placemin),
        ('М+', placeplus),
        ('П-', behaviourmin),
        ('П+', behaviourplus),
    )

    CHOICES_BOOLEAN_YES_NO = (
        (True, _('Да')),
        (False, _('Нет'))
    )

    owner = models.ForeignKey(StaffGroup,
                              verbose_name="создатель наблюдения",
                              on_delete=models.PROTECT,
                              related_name='owners', )

    users_organization = models.ForeignKey(Organization,
                                           verbose_name="Организация",
                                           on_delete=models.PROTECT,
                                           related_name='users_organization',
                                           null=True,
                                           blank=True,
                                           default='')

    users_department = models.ForeignKey(Department,
                                         verbose_name="Ваш участок",
                                         on_delete=models.PROTECT,
                                         related_name="users_department",
                                         null=True,
                                         blank=True,
                                         default='')

    date_viewed = models.DateField(verbose_name='Дата наблюдения', default=date.today)

    category = models.ForeignKey(Category,
                                 verbose_name="Категория",
                                 on_delete=models.PROTECT,
                                 related_name='categories')

    character = models.CharField(choices=CHARACTER_CHOICES,
                                 verbose_name="Характер наблюдения",
                                 null=False,
                                 blank=False,
                                 default='',
                                 max_length=35,
                                 )

    dialog = models.BooleanField(verbose_name="Был диалог (да/нет)",
                                 choices=CHOICES_BOOLEAN_YES_NO,
                                 blank=True,
                                 )

    view = models.ForeignKey(View,
                             verbose_name="Вид наблюдения",
                             on_delete=models.PROTECT,
                             related_name='views',
                             null=True,
                             blank=True)
    site = models.ForeignKey(Site,
                              verbose_name="Участок наблюдения",
                              on_delete=models.PROTECT,
                              related_name='sites')

    place = models.ForeignKey(Place,
                             verbose_name="Место наблюдения",
                             on_delete=models.PROTECT,
                             related_name='places',
                             null=True,
                             blank=True
                        )

    description = models.TextField("Описание", max_length=1000)

    probability = models.PositiveSmallIntegerField("Вероятность (от 0 до 5)",
                                                   default=0,
                                                   validators=[MaxValueValidator(5), MinValueValidator(0)],
                                                   null=True)

    effects = models.PositiveSmallIntegerField("Последствия (от 0 до 5)",
                                               default=0,
                                               validators=[MaxValueValidator(5), MinValueValidator(0)],
                                               null=True)

    risk = models.PositiveSmallIntegerField("Уровень риска",
                                            blank=True,
                                            default=0, )

    correction = models.TextField("Улучшение\Влияние", max_length=256, blank=True)

    control = models.ForeignKey(Control,
                                verbose_name="Контроль",
                                on_delete=models.PROTECT,
                                related_name='controls',
                                null=True,
                                blank=True)

    manager = models.ForeignKey(Employee,
                                verbose_name="Ответственный руководитель",
                                on_delete=models.PROTECT,
                                related_name='managers',
                                blank=True,
                                null=True,
                                )

    date_closed_target = models.DateField('Дата закрытия - цель')

    date_closed_fact = models.DateField('Дата закрытия - факт', null=True, blank=True)

    status = models.CharField(verbose_name="Статус",
                              choices=STATUS_CHOICES,
                              max_length=15,
                              default='New')

    date_created = models.DateField(default=date.today)

    corr_action = models.TextField('Корректирующие мероприятия', max_length=512, blank=True)

    photo1 = models.ImageField('Фото1', upload_to='photos/%Y/%m/%d', blank=True)
    photo2 = models.ImageField('Фото2', upload_to='photos/%Y/%m/%d', blank=True)
    photo3 = models.ImageField('Фото3', upload_to='photos/%Y/%m/%d', blank=True)
    photo4 = models.ImageField('Фото4', upload_to='photos/%Y/%m/%d', blank=True)
    photo5 = models.ImageField('Фото5', upload_to='photos/%Y/%m/%d', blank=True)

    class Meta:
        verbose_name = 'Наблюдение по безопасности'
        verbose_name_plural = 'Наблюдения по безопасности'
        ordering = ['-id']
