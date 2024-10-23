from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),

    path('password_change/', views.password_change, name='password_change'),
    path('password-change/done/', views.password_change_done, name='password_change_done'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/uidb64/token/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),

    path('personal_account_main/', views.personal_account_main, name='personal_account_main'),
    path('order_an_individual_course/', views.order_an_individual_course, name='order_an_individual_course'),
    path('order_an_individual_course/done/', views.order_an_individual_course_done,
         name='order_an_individual_course_done'),

    path('rating/', views.rating, name='rating'),
]
