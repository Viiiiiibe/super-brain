from django.shortcuts import render


def signup(request):
    return render(request, 'account/signup.html')


def logout(request):
    return render(request, 'account/logout.html')


def login(request):
    return render(request, 'account/login.html')


def password_change(request):
    return render(request, 'account/password_change_form.html')


def password_change_done(request):
    return render(request, 'account/password_change_done.html')


def password_reset(request):
    return render(request, 'account/password_reset_form.html')


def password_reset_done(request):
    return render(request, 'account/password_reset_done.html')


def password_reset_confirm(request):
    return render(request, 'account/password_reset_confirm.html')


def password_reset_complete(request):
    return render(request, 'account/password_reset_complete.html')


def personal_account_main(request):
    return render(request, 'account/personal_account_main.html')


def order_an_individual_course(request):
    return render(request, 'account/order_an_individual_course.html')


def order_an_individual_course_done(request):
    return render(request, 'account/order_an_individual_course_done.html')
