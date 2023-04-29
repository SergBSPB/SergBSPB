from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterMixin
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Count, F, Q, Max, Min, Sum, Exists, Subquery, Aggregate
import pandas as pd

from .filters import ObservationsFilter
from .forms import *
from .models import *
from dynamic_forms import DynamicField, DynamicFormMixin

import plotly.express as px

User = get_user_model()


def index(request):
    return render(request, 'observations/index.html')


def buttons(request):
    return render(request, 'observations/two_buttons.html')


def success(request):
    return render(request, 'observations/success_url.html')


class AddPage(LoginRequiredMixin, CreateView, DynamicFormMixin, forms.Form):
    form_class = AddItemForm
    template_name = 'observations/addpage.html'
    success_url = reverse_lazy('success')
    login_url = reverse_lazy('home')

    # def place_choices(self, form):
    #     site = form.fields['site'].value()
    #     print(site)
    #     return Place.objects.filter(site_place=site)


    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.owner = self.request.user
        u = Employee.objects.get(user=self.request.user)
        form.instance.users_organization = u.users_organization
        form.instance.users_department = u.users_department
        if form.instance.manager is None:
            form.instance.manager = Employee.objects.filter(user_id=form.instance.site.sites_manager.id).first()
        response = super().form_valid(form)
        subject = 'Наблюдение по безопасности №' + str(form.instance.id) + '-' + 'СОЗДАНИЕ'
        message = str(form.instance.description) + '  ' + 'http://127.0.0.1:8000/observations/' + str(
            form.instance.id)
        if form.instance.risk > 15:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [form.instance.owner.email, form.instance.manager.user.email],
            )
            email.send()
        else:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [form.instance.owner.email],
            )
            email.send()
        return response

    def get_form(self, form_class=None):

        # def place_choices(form):
        #     site = form['site'].value()
        #     print(site)
        #     return Place.objects.filter(site_place=site)

        form = super().get_form(form_class=form_class)
        # form.fields['manager'].queryset = StaffGroup.objects.filter(groups__id=area_manager.id)
        u = Employee.objects.get(user=self.request.user)
        form.fields['manager'].queryset = Employee.objects.filter(is_manager=True,
                                                                  users_organization__id=u.users_organization.id)
        form.fields['site'].queryset = Site.objects.filter(sites_organisation__id=u.users_organization.id)
       ## form.fields['place'] = DynamicField(forms.ModelChoiceField, queryset=place_choices)

        # form.fields['place'].queryset = Place.objects.filter(place_organisation__id=u.users_organization.id)
        form.fields["users_organization"].initial = u.users_organization
        form.fields['users_department'].initial = u.users_department
        view_number = View.objects.get(id=9)
        form.fields['view'].initial = view_number

        # if u.users_organization.id != 2:
        #     form.fields.pop("place")
        return form


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'observations/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'observations/login.html'
    next_page = reverse_lazy('buttons')


def logout_user(request):
    logout(request)
    return redirect('login')


class ObservationsListView(LoginRequiredMixin, FilterMixin, ListView):
    queryset = Observation.objects.all()
    template_name = 'observations/list_observations.html'
    filterset_class = ObservationsFilter
    login_url = reverse_lazy('home')

    strict = False

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        if self.filterset.is_valid() or not self.get_strict():
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        manager_choise = Employee.objects.filter(user_id=self.request.user.id)
        responsible_status = Employee.objects.get(user_id=self.request.user.id)
        manager_check = responsible_status.is_manager

        manager_total = Observation.objects.filter(manager__in=manager_choise).aggregate(
            new=Count('id', filter=Q(status='New')),
            open=Count('id', filter=Q(status='New') | Q(status='Progress'))
            # open=Count('id', filter=~Q(status='Completed'))
        )
        # manager_total_new = Observation.objects.filter(manager__in=manager_choise, status='New').count()
        # manager_total_open = Observation.objects.filter(manager__in=manager_choise).exclude(status='Completed').count()

        context = self.get_context_data()
        context.update({
            'filter_form': self.filterset.form,
            'manager_total': manager_total,
            'manager_check': manager_check,
        })

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        """ owner=self.request.user - Отображает только записи залогининого пользователя - руководителя наблюдений"""
        manager_employee_choise = Employee.objects.filter(user_id=self.request.user.id)
        queryset = queryset.filter(users_organization__id__in=manager_employee_choise.values('users_organization_id'))
        return queryset


class AdvancedListView(LoginRequiredMixin, FilterMixin, ListView):
    queryset = Observation.objects.all()
    template_name = 'observations/advanced_list.html'
    filterset_class = ObservationsFilter
    login_url = reverse_lazy('home')

    strict = False

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        if self.filterset.is_valid() or not self.get_strict():
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        manager_choise = Employee.objects.filter(user_id=self.request.user.id)
        responsible_status = Employee.objects.get(user_id=self.request.user.id)
        manager_check = responsible_status.is_manager
        users_organization_form_id = responsible_status.users_organization.id
        manager_total = Observation.objects.filter(manager__in=manager_choise).aggregate(
            new=Count('id', filter=Q(status='New')),
            open=Count('id', filter=~Q(status='Completed'))
        )

        context = self.get_context_data()
        context.update({
            'filter_form': self.filterset.form,
            'manager_total': manager_total,
            'manager_check': manager_check,
            'users_organization_form_id': users_organization_form_id
        })

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        """ owner=self.request.user - Отображает только записи залогининого пользователя - руководителя наблюдений"""
        manager_employee_choise = Employee.objects.filter(user_id=self.request.user.id)
        queryset = queryset.filter(users_organization__id__in=manager_employee_choise.values('users_organization_id'))
        return queryset


class ManagerObservationsListView(LoginRequiredMixin, FilterMixin, ListView):
    queryset = Observation.objects.all()
    template_name = 'observations/manager_observations.html'
    filterset_class = ObservationsFilter
    login_url = reverse_lazy('home')

    strict = False

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        if self.filterset.is_valid() or not self.get_strict():
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        manager_choise = Employee.objects.filter(user_id=self.request.user.id)
        responsible_status = Employee.objects.get(user_id=self.request.user.id)
        manager_check = responsible_status.is_manager

        manager_total = Observation.objects.filter(manager__in=manager_choise).aggregate(
            new=Count('id', filter=Q(status='New')),
            open=Count('id', filter=~Q(status='Completed'))
        )

        context = self.get_context_data()
        context.update({
            'manager_total': manager_total,
            'manager_check': manager_check,
        })

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        """ owner=self.request.user - Отображает только записи залогининого пользователя - руководителя наблюдений"""
        manger_employee_choise = Employee.objects.filter(user_id=self.request.user.id)
        queryset = queryset.filter(manager__id__in=manger_employee_choise)
        return queryset


class EmployeeObservationsListView(LoginRequiredMixin, FilterMixin, ListView):
    queryset = Observation.objects.all()
    template_name = 'observations/employee_observation.html'
    filterset_class = ObservationsFilter
    login_url = reverse_lazy('home')

    strict = False

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        if self.filterset.is_valid() or not self.get_strict():
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        manager_choise = Employee.objects.filter(user_id=self.request.user.id)
        responsible_status = Employee.objects.get(user_id=self.request.user.id)
        manager_check = responsible_status.is_manager

        manager_total = Observation.objects.filter(manager__in=manager_choise).aggregate(
            new=Count('id', filter=Q(status='New')),
            open=Count('id', filter=~Q(status='Completed'))
        )

        context = self.get_context_data()
        context.update({
            'manager_total': manager_total,
            'manager_check': manager_check,
        })
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        """ owner=self.request.user - Отображает только записи залогининого пользователя - иницииатора наблюдения"""
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ObservationDetailView(LoginRequiredMixin, DetailView):
    model = Observation
    template_name = 'observations/detail_observation.html'
    pk_url_kwarg = 'observation_id'
    context_object_name = 'observation'
    login_url = reverse_lazy('home')


def pageNotFound(request, exception):
    return HttpResponse('<h1>Страницы не существует!</h1>')


class ObservationAdditionView(LoginRequiredMixin, UpdateView):
    model = Observation
    template_name = 'observations/addition_observation.html'
    pk_url_kwarg = 'observation_id'
    context_object_name = 'observation'
    form_class = ObservationAdditionForm
    success_url = reverse_lazy('list_observation')
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object.description += ' ' + str(date.today().strftime('%d-%m-%Y')) + ' ' + form.cleaned_data['addition']
        response = super().form_valid(form)
        subject = 'Наблюдение по безопасности №' + str(form.instance.id) + '-' + 'ДОПОЛНЕНО ОПИСАНИЕ'
        message = str(form.instance.description) + '  ' + 'http://10.10.10.16:8000/observations/' + str(
            form.instance.id)
        if form.instance.risk > 15:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [form.instance.owner.email, form.instance.manager.user.email],
            )
            email.send()
        else:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [form.instance.owner.email],
            )
            email.send()
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        """ owner=self.request.user - Отображает только записи залогининого пользователя"""
        try:
            queryset = queryset.filter(owner=self.request.user,
                                       # date_closed_fact__isnull=True
                                       )
        except:
            raise Http404()
        return queryset


class ObservationCloseView(LoginRequiredMixin, UpdateView):
    model = Observation
    template_name = 'observations/close_observation.html'
    pk_url_kwarg = 'observation_id'
    context_object_name = 'observation'
    form_class = ObservationCloseForm
    success_url = reverse_lazy('manager_observation')
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object.description += ' ' + str(date.today().strftime('%d-%m-%Y')) + ' ' + form.cleaned_data['addition']
        self.object.correction += ' ' + str(date.today().strftime('%d-%m-%Y')) + ' ' \
                                  + form.cleaned_data['improvement_addition']

        if form.instance.status == Observation.STATUS_COMPLETED:
            form.instance.date_closed_fact = date.today()

        response = super().form_valid(form)
        change_subject = 'Наблюдение по безопасности №' + str(form.instance.id) + '- ' + 'ИЗМЕНЕНО РУКОВОДИТЕЛЕМ'
        closed_subject = 'Наблюдение по безопасности №' + str(form.instance.id) + '- ' + 'ЗАКРЫТО'

        if form.instance.status == Observation.STATUS_COMPLETED:
            subject = closed_subject
        else:
            subject = change_subject

        message = str(form.instance.corr_action) + '  ' + 'http://10.10.10.16:8000/observations/' + str(
            form.instance.id)
        if form.instance.risk > 15:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [form.instance.owner.email, form.instance.manager.user.email],
            )
            email.send()
        else:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [form.instance.owner.email],
            )
            email.send()

        return response

    def get_form(self, form_class=None):
        """Руководитель может выбрать другого руководителя из этой же организации"""

        form = super().get_form(form_class=form_class)
        u = Employee.objects.get(user=self.request.user)
        form.fields['manager'].queryset = Employee.objects.filter(is_manager=True,
                                                                  users_organization__id=u.users_organization.id)
        form.fields['users_department'].queryset = Department.objects.filter(id=self.object.users_department_id)
        form.fields['users_organization'].queryset = Organization.objects.filter(id=self.object.users_organization_id)
        form.fields['site'].queryset = Site.objects.filter(sites_organisation__id=u.users_organization.id)
        form.fields['place'].queryset = Place.objects.filter(place_organisation__id=u.users_organization.id)
        return form


# Представление для отображения отчётов в виде графиков
def owner_observation_count(request):
    form = ReportForm(request.GET)
    context = {}
    if form.is_valid():
        organisation = form.cleaned_data['organisation']

        view_chart = Observation.objects.values('view__name').annotate(view_count=Count('view_id'))
        owner_chart = Observation.objects.values('owner__last_name').annotate(owner_count=Count('owner_id'))
        owner_chart_2 = Observation.objects.values('owner__last_name', 'category__name').annotate(
            owner_count_2=Count('owner_id'))
        area_chart = Observation.objects.values('site__name__name').annotate(area_count=Count('site_id'))
        observations_count = Observation.objects.values('id')

        if organisation:
            view_chart = view_chart.filter(users_organization=organisation)
            owner_chart = owner_chart.filter(users_organization=organisation)
            owner_chart_2 = owner_chart_2.filter(users_organization=organisation)
            area_chart = area_chart.filter(users_organization=organisation)
            observations_count = observations_count.filter(users_organization=organisation)

        start = form.cleaned_data['start']
        end = form.cleaned_data['end']

        if start:
            view_chart = view_chart.filter(date_created__gte=start)
            owner_chart = owner_chart.filter(date_created__gte=start)
            owner_chart_2 = owner_chart_2.filter(date_created__gte=start)
            area_chart = area_chart.filter(date_created__gte=start)
            observations_count = observations_count.filter(date_created__gte=start)
        if end:
            view_chart = view_chart.filter(date_created__lte=end)
            owner_chart = owner_chart.filter(date_created__lte=end)
            owner_chart_2 = owner_chart_2.filter(date_created__lte=end)
            area_chart = area_chart.filter(date_created__lte=end)
            observations_count = observations_count.filter(date_created__lte=end)

        obs_count = observations_count.count()
        area_data_pd = pd.DataFrame.from_dict(area_chart)
        area_data_pd.columns = ['Участок наблюдения', 'Количество']

        view_data_pd = pd.DataFrame.from_dict(view_chart)
        view_data_pd.columns = ['Вид наблюдения', 'Количество']

        owner_x = owner_chart.values_list('owner__last_name', flat=True)
        owner_y = owner_chart.values_list('owner_count', flat=True)

        fig_0 = px.pie(view_data_pd, values='Количество', names='Вид наблюдения', title='Виды наблюдений')
        fig_0.update_layout(title={
            'font_family': "Rockwell",
            'font_size': 25,
            'y': 0.9,
            'x': 0.5,
             })
        chart_0 = fig_0.to_html()

        fig = px.bar(
            x=owner_x,
            y=owner_y,
            text_auto='.0f',
            title='Количество наблюдений созданных сотрудниками',
            labels={'y': 'Количество наблюдений', 'x': 'Сотрудники'}
        )
        fig.update_layout(title={
            'font_family': "Rockwell",
            'font_size': 25,
            'y': 0.9,
            'x': 0.5,
             })
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        chart = fig.to_html()

        fig_2 = px.pie(area_data_pd, values='Количество', names='Участок наблюдения', title='Наблюдения в участках')
        fig_2.update_layout(title={
            'font_family': "Rockwell",
            'font_size': 25,
            'y': 0.9,
            'x': 0.5,
             })
        chart_2 = fig_2.to_html()

        context.update({'chart_0': chart_0, 'chart': chart, 'chart_2': chart_2, 'pd_table': owner_chart_2,
                        'obs_count': obs_count})
    context['form'] = form
    return render(request, 'observations/reports.html', context)
