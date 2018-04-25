# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q, F
from django.contrib.auth.models import User

from utils import http
from config import codes

logger = logging.getLogger(__name__)

def show_user_index_view(request, user_id=None):
    return render(request, "user/index.html", locals()) 
