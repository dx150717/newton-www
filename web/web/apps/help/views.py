from django.shortcuts import render


def show_help_view(request):
    return render(request, "help/security.html")