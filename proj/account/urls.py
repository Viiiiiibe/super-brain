from django.urls import path
from . import views
from django.contrib.auth.views import (
    LogoutView, PasswordChangeDoneView,
    PasswordResetDoneView, PasswordResetCompleteView
)

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path('login/', views.LoginView.as_view(), name='login'),
    path(
        'password_change/',
        views.UserPasswordChange.as_view(template_name='account/password_change_form.html'),
        name='password_change'
    ),
    path(
        'password-change/done/',
        PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
        name='password_change_done'
    ),

    path(
        'password_reset/',
        views.UserPasswordResetView.as_view(template_name='account/password_reset_form.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
        name='password_reset_complete'
    ),


    path('personal_account_main/', views.personal_account_main, name='personal_account_main'),
    path('order_an_individual_course/', views.order_an_individual_course, name='order_an_individual_course'),
    path('order_an_individual_course/done/', views.order_an_individual_course_done,
         name='order_an_individual_course_done'),

    path('rating/', views.rating, name='rating'),
]
