from django.shortcuts import render


def our_team(request):
    return render(request, 'about/our_team.html')


def contacts(request):
    return render(request, 'about/contacts.html')


def faq(request):
    return render(request, 'about/faq.html')
