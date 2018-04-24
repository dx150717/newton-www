from django.shortcuts import render
from forms import KycForm
# Create your views here.
def index(request):
    form = KycForm()
    return render(request, "newtonadmin/index.html", locals())
