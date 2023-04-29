from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django.urls import reverse_lazy

from .models import *


class AddItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('home')
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('submit', 'Добавить'))


    class Meta:

        model = Observation
        fields = '__all__'
        exclude = ['date_closed_fact', 'date_created', 'owner', 'corr_action', 'control', 'status', 'photo4', 'photo5']
        widgets = {
            'users_organization': forms.Select(attrs={'disabled': True}),
            'users_department': forms.Select(attrs={'disabled': True}),
            'date_viewed': forms.TextInput(attrs={'max': date.today, 'value': date.today, 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'character': forms.RadioSelect(),
            'dialog': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view': forms.Select(attrs={'class': 'form-select'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
            # 'place': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 5, 'placeholder': 'Введите описание наблюдения'}),
            'risk': forms.TextInput(attrs={'readonly': True}),
            'correction': forms.Textarea(attrs={'cols': 60, 'rows': 5, 'placeholder': 'На что может повлиять'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'date_closed_target': forms.DateInput(attrs={'min': date.today, 'type': 'date'}),
        }


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'cols': 30, 'rows': 3,
                                                             'class': 'form-control form-control-sm'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'cols': 30, 'rows': 3,
                                                                 'class': 'form-control form-control-sm'}))


class ObservationAdditionForm(forms.ModelForm):
    addition = forms.CharField(label='Дополнение в поле Описание:',
                               widget=forms.Textarea(
                                   attrs={'placeholder': 'Здесь можете внести дополнение в описание наблюдения'}))

    class Meta:
        model = Observation
        fields = ('addition',)
        widgets = {'addition': forms.Textarea(attrs={'cols': 40, 'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Добавить'))


class ObservationCloseForm(forms.ModelForm):
    addition = forms.CharField(label='Дополнение в поле Описание:', required=False,
                               widget=forms.Textarea(
                                   attrs={'cols': 60, 'rows': 3,
                                          'placeholder': 'Здесь можете внести дополнение в описание наблюдения'}))

    improvement_addition = forms.CharField(label='Дополнение в поле Улучшение\Влияние:', required=False,
                                           widget=forms.Textarea(
                                               attrs={'cols': 60, 'rows': 3,
                                      'placeholder': 'Здесь можете внести дополнение в описание Улучшение \ Влияние'}))

    class Meta:
        model = Observation
        fields = '__all__'
        exclude = ['date_created', 'photo1', 'owner', 'photo2', 'photo3']
        widgets = {
            # 'owner': forms.Select(attrs={'disabled': True}),
            'users_organization': forms.Select(attrs={'disabled': True}),
            'users_department': forms.Select(attrs={'disabled': True}),
            'date_viewed': forms.TextInput(attrs={'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'character': forms.RadioSelect(),
            'dialog': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view': forms.Select(attrs={'class': 'form-select'}),
            'site': forms.Select(attrs={'class': 'form-select'}),
            'place': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'readonly': True}),
            'risk': forms.TextInput(attrs={'readonly': True}),
            'correction': forms.Textarea(attrs={'readonly': True}),
            'control': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_closed_target': forms.TextInput(attrs={'readonly': True}),
            'date_closed_fact': forms.DateInput(attrs={'type': 'date'}),
            'corr_action': forms.Textarea(attrs={'cols': 60, 'rows': 3}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Добавить'))


class ReportForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('home')
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'GET'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-5'
        self.helper.layout = Layout(
            Row(
                Column('start'),
                Column('end'),
            ),
            Row(
                Column('organisation')
            )
        )
        self.helper.add_input(Submit('submit', 'Применить'))

    start = forms.DateField(label='От:', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end = forms.DateField(label='До:', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    organisation = forms.ModelChoiceField(label='Организация:', queryset=Organization.objects.all(), required=False)