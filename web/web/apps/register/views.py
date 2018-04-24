from django.shortcuts import render,redirect
from django.core.validators import validate_email
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from utils import http,security
from user import models as user_model
from subscription import task as register_task
from django.template import Template,Context,loader
from config import codes
import settings
import logging
import forms
logger = logging.getLogger(__name__)

def show_register_view(request):
    return render(request, 'register/index.html', locals())

def postemail(request):
    try:
        if request.method == "POST":
            was_limited = getattr(request, 'limited', False)
            if not was_limited:
                email_address = request.POST['email']
                validate_email(email_address)
                user = User.objects.filter(email = email_address).first()
                if user is not None:
                    profile = user_model.UserProfile.objects.filter(user = user).first()
                    if profile is not None and profile.is_email_verified:
                        result = http.JsonErrorResponse(error_message = _('Email Has Exist!'))
                    else:
                        send_flag = do_send_mail(user,request)
                        if send_flag:
                            result = http.JsonSuccessResponse(data = {"msg": _("we've sent you a confirming e-mail,please check your email box.")})
                        else:
                            result = http.JsonErrorResponse(error_message = _("Register Failed!"))
                else:
                    username = security.generate_uuid()
                    userobj = User.objects.create_user(username, email=email_address)
                    profile = user_model.UserProfile(user=userobj)
                    profile.save()
                    send_flag = do_send_mail(userobj,request)
                    if send_flag:
                        result = http.JsonSuccessResponse(data = {"msg": _("we've sent you a confirming e-mail,please check your email box.")})
                    else:
                        result = http.JsonErrorResponse(error_message = _("Register Failed!"))
            else:
                result = http.JsonErrorResponse(error_message = _("You can only send email once per minute."))
            return result
        else:
            return render(request, 'register/index.html', locals())
    except ValidationError:
        return http.JsonErrorResponse(error_message = _("Invalid Email Address!"))
    except Exception,inst:
        print("error on register view %s" %str(inst))
        return http.JsonErrorResponse()


def show_verify_view(request):
    try:
        id = request.GET['uuid']
        return redirect("/register/editpassword/?id=%s" %(id))
        user = User.objects.filter(id=id).first()
        if user is None:
            return redirect("/register/")
        else:
            profile = user_model.UserProfile.objects.filter(user=user).first()
            profile.is_email_verified = True
            profile.save()
            return redirect("/register/editpassword/?id=%s" %(id))
    except Exception,inst:
        print("confiremd error: %s" %(str(inst)))
        return http.JsonErrorResponse(error_message = _("error"))


def show_editpassword_view(request):
    #id = request.GET['id']
    template_name = 'register/register-form.html'
    return render(request, template_name, locals())



def postpassword(request):
    return redirect("/user/edit/")
    try:
        if request.method == 'POST':
            password = request.POST['password']
            repassword = request.POST['repassword']
            id = request.POST['id']
            #TODO need validate password
            user = User.objects.filter(id=id).first()
            user.set_password(password)
            user.save()
            authed_user = authenticate(username = user.username, password = password)
            if authed_user is not None:
                login(request, authed_user)
                #TODO set session
                return redirect("/user/edit/")
            else:
                print("user authed_user is null")
                return http.JsonErrorResponse(error_message = _("error"))
            return http.JsonSuccessResponse(data="success")
        else:
            return http.JsonErrorResponse(error_message = _("error"))
    except Exception,inst:
        print("error on password:%s" %(inst))
        return http.JsonErrorResponse(error_message = _("error"))



# valid email
def do_send_mail(user,request):
    subject = _("NewtonProject Notifications: Please Register")
    targetUrl = "http://localhost:8000" + "/register/verify/?uuid=" + str(user.id)
    try:
        template = loader.get_template("register/register-letter.html")
        context = Context({"targetUrl":targetUrl,"request":request})
        html_content = template.render(context)
        to_email = user.email
        from_email = settings.FROM_EMAIL
        register_task.send_email.delay(subject,html_content,from_email,[to_email])
        return True
    except Exception,inst:
        print("fail to send email: %s" % str(inst))
        return False