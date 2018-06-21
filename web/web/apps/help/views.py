from django.shortcuts import render


def show_security_view(request):
    return render(request, "help/security.html")