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


    path('personal_account_main/', views.personal_account_main, name='personal_account_main'),
    path('order_an_individual_course/', views.order_an_individual_course, name='order_an_individual_course'),
    path('order_an_individual_course/done/', views.order_an_individual_course_done,
         name='order_an_individual_course_done'),

    path('rating/', views.rating, name='rating'),
]
