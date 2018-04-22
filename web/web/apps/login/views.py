from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from utils import http,security
from user import models as user_model


def show_login_view(request):
    if request.method == "POST":
        try:
            print("post")
            email = request.POST.get("email",None)
            print(email)
            password = request.POST.get("password",None)
            print(password)
            user = User.objects.get(email=email)
            if user is not None:
                authed_user = authenticate(username=user.username,password=password)
                if authed_user is not None:
                    login(request, authed_user)
                    return redirect("/")
                else:
                    return http.JsonErrorResponse(error_message = _("Password error"))
            else:
                return http.JsonErrorResponse(error_message = _("Email not exist !"))
        except Exception,inst:
            print("error auth:%s" %(str(inst)))
            return http.JsonErrorResponse(error_message = _("error")) 
    else:
        print("get")
        return render(request, 'login/index.html', locals())
