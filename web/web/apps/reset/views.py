from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from utils import http,security
from django.template import Template,Context,loader
from config import codes
from tasks import task_email
import settings
import logging
logger = logging.getLogger(__name__)


def show_repassword_view(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email", None)
            user = User.objects.get(email = email)
            if user is not None:
                send_flag =  do_send_mail(user, request)
                if send_flag:
                    return redirect("/")
                else:
                    return http.JsonErrorResponse(error_message = _("send Email error!"))
            else:
                # TODO register
                return http.JsonErrorResponse(error_message = _("Email not exist!"))
        else:
            return render(request,'reset/index.html', locals())
    except Exception,inst:
        print("error repassword: %s" %(str(inst)))
    


def show_edit_password_view(request):
    return render(request,'reset/edit_password.html', locals())
    try:
        if request.method == "POST":
            id = request.POST.get("id",None)
            user = User.objects.get(id=id)
            if user is None:
                return http.JsonErrorResponse(error_message = _("User not exist!"))
            else:
                password = request.POST.get("password",None)
                repassword = request.POST.get("repassword",None)
                if password == repassword:
                    user.set_password(password)
                    user.save()
                    return redirect("/")
                else:
                    return http.JsonErrorResponse(error_message = _("Password error"))
        else:
            if request.method == "GET":
                id = request.GET.get("u",None)
                if id is not None:
                    print("id is %s" %str(id))
                    user = User.objects.get(id=id)
                    print(user)
                    if user is not None:
                        return render(request,'reset/edit_password.html', locals())
                    else:
                        return http.JsonErrorResponse(error_message = _("User not exist!"))
                else:
                    return http.JsonErrorResponse(error_message = _("User not exist!"))
            else:
                return redirect("/")
    except Exception,inst:
        print("error edit password :%s" %(str(inst)))
    
        


# valid email
def do_send_mail(user,request):
    subject = _("NewtonProject Notifications: Please Repassword")
    targetUrl = "http://localhost:8000" + "/reset/edit_password/?u=" + str(user.id)
    try:
        template = loader.get_template("subscription/subscription-letter.html")
        context = Context({"targetUrl":targetUrl,"request":request})
        html_content = template.render(context)
        to_email = user.email
        from_email = settings.FROM_EMAIL
        task_email.send_email.delay(subject,html_content,from_email,[to_email])
        return True
    except Exception,inst:
        print("fail to send email: %s" % str(inst))
        return False
