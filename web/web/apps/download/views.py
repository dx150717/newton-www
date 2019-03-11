# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation

logger = logging.getLogger(__name__)


def show_newpay_download_view(request):
    code = request.GET.get('code', '')
    if code:
        return render(request, "download/newpay-download-invite.html", locals())
    else:
        return redirect('/newpay/')


def show_newpay_guide_view(request):
    return render(request, "download/newpay-guide.html", locals())
