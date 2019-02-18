from django.shortcuts import render

import logging

logger = logging.getLogger(__name__)


def show_newpay_download_view(request):
    code = request.GET.get('code', '')
    if code:
        return render(request, "download/newpay-download-invite.html", locals())
    else:
        return render(request, "download/newpay-download.html", locals())

def show_newpay_guide_view(request):
    return render(request, "download/newpay-guide.html", locals())
