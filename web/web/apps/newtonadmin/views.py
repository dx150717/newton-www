from django.shortcuts import render, redirect

def show_login_view(request):
    return render(request, "login.html", locals())

def post_login(request):
    return redirect("/newtonadmin/")

def logout(request):
    return redirect("/")

def index(request):
    return render(request, "newtonadmin/welcome.html", locals())

def kyc_admin(request):
    return render(request, "newtonadmin/kycindex.html", locals())

def kyc_detail(request):
    return render(request, "newtonadmin/kycdetail.html", locals())

def kyc_update(request):
    update_info = "Update Successed!"
    return render(request, "newtonadmin/kycdetail.html", locals());

def kyc_send_email(request):
    update_info = "Send Successed!"    
    return render(request, "newtonadmin/kycindex.html", locals());

def kyc_export_csv(request):
    update_info = "Export Successed!"    
    return render(request, "newtonadmin/kycindex.html", locals());

def blog_admin(request):
    return render(request, "index.html", locals())
