from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', LoginUser.as_view(), name='home'),
    # path('index/', index, name='index'),
    path('two_buttons/', buttons, name='buttons'),
    path('success_url/', success, name='success'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('observations/', ObservationsListView.as_view(), name='list_observation'),
    path('advanced_observations/', AdvancedListView.as_view(), name='advanced_list'),
    path('manager_observations/', ManagerObservationsListView.as_view(), name='manager_observation'),
    path('employee_observation/', EmployeeObservationsListView.as_view(), name='employee_observation'),
    path('observations/<int:observation_id>/', ObservationDetailView.as_view(), name='detail_observation'),
    path('observations/<int:observation_id>/addition/', ObservationAdditionView.as_view(), name='addition_observation'),
    path('reports/', owner_observation_count, name='report'),
    path('observations/<int:observation_id>/close/', ObservationCloseView.as_view(), name='close_observation'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='observations/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='observations/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='observations/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='observations/password_reset_done.html'),
         name='password_reset_complete'),
]