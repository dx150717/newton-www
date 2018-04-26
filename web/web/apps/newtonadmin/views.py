# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

def show_login_view(request):
    return render(request, "login.html", locals())

def post_login(request):
    return redirect("/newtonadmin/")

def logout(request):
    return redirect("/")

def index(request):
    return render(request, "newtonadmin/welcome.html", locals())

