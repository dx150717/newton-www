from django.shortcuts import render

import logging

logger = logging.getLogger(__name__)


def show_newpay_download_view(request):
    return render(request, "download/newpay-download.html", locals())
