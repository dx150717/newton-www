# -*- coding: utf-8 -*-
import logging

import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.contrib.auth.models import User
from django.views import generic
from django.db.models import Sum
from django_countries.data import COUNTRIES
from django.db.models import Q

from utils import http
from utils import convert
from utils import exception
from config import codes
from tokenexchange import models as tokenexchange_models
from tracker import models as tracker_models
from newtonadmin import models as newtonadmin_models
from . import forms_tokenexchange
from . import services_tokenexchange

logger = logging.getLogger(__name__)

def build_query_condition(request, q):
    """Build the query condition
    """
    kyc_type = request.GET.get('kyc_type')
    is_establish_node = request.GET.get('is_establish_node')
    country = request.GET.get('country')
    if kyc_type:
        kyc_type = int(kyc_type)
        q &= Q(kyc_type=kyc_type)
    if is_establish_node:
        is_establish_node = int(is_establish_node)
        q &= Q(is_establish_node=is_establish_node)
    if country:
        q &= Q(country=country)
    return q

def extract_query_parameter(request):
    """Extract the query parameter
    """
    result = {}
    kyc_type = request.GET.get('kyc_type')
    is_establish_node = request.GET.get('is_establish_node')
    country = request.GET.get('country')
    if kyc_type:
        kyc_type = int(kyc_type)
        result['kyc_type'] = kyc_type
    if is_establish_node:
        is_establish_node = int(is_establish_node)
        result['is_establish_node'] = is_establish_node
    if country:
        result['country'] = country
    return result

class IdListView(generic.ListView):
    template_name = "newtonadmin/id-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(IdListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(IdListView, self).get_context_data(**kwargs)
        context['level_choices'] = [i+1 for i in range(10)]
        context['is_idlist'] = True
        context['countries_choices'] = COUNTRIES
        context['title'] = '待审核'
        return context

    def get_queryset(self):
        try:

            fields = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.CANDIDATE.value)
            items = []
            if fields and len(fields) > 0:
                for item in fields:
                    if item.id_type:
                        item.id_type = convert.get_value_from_choice(item.id_type, tokenexchange_models.ID_CHOICES)
                    item.country = COUNTRIES[item.country]
                    items.append(item)
            return items
        except Exception, inst:
            logger.exception("fail to show id list:%s" % str(inst))
            return None


class PassIdListView(generic.ListView):
    template_name = "newtonadmin/id-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(PassIdListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(PassIdListView, self).get_context_data(**kwargs)
        context['countries_choices'] = COUNTRIES
        context['title'] = '已通过'
        return context

    def get_queryset(self):
        try:
            fields = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.PASS_KYC.value)
            items = []
            if fields and len(fields) > 0:
                for item in fields:
                    if item.id_type:
                        item.id_type = convert.get_value_from_choice(item.id_type, tokenexchange_models.ID_CHOICES)
                    item.country = COUNTRIES[item.country]
                    items.append(item)
            return items
        except Exception, inst:
            logger.exception("fail to show pass id list:%s" % str(inst))
            return None


class InviteListView(generic.ListView):
    template_name = "newtonadmin/te-waiting-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(InviteListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(InviteListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        query_form = forms_tokenexchange.KYCQueryForm(initial=extract_query_parameter(self.request))
        context['query_form'] = query_form
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            s1 = set(tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.PASS_KYC.value).values_list('user_id', flat=True))
            s2 = set(tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id).values_list('user_id', flat=True))
            d = s1.difference(s2)
            q = Q(status=codes.KYCStatus.PASS_KYC.value, user_id__in=d)
            q = build_query_condition(self.request, q)
            items = tokenexchange_models.KYCInfo.objects.filter(q).order_by('-level')
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show invite list:%s" % str(inst))
            return None
    

class CompletedInviteListView(generic.ListView):
    template_name = "newtonadmin/te-completed-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(CompletedInviteListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(CompletedInviteListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        query_form = forms_tokenexchange.KYCQueryForm(initial=extract_query_parameter(self.request))
        context['query_form'] = query_form
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            q = Q(phase_id=phase_id, status__in=[codes.TokenExchangeStatus.INVITE.value, codes.TokenExchangeStatus.SEND_INVITE_NOTIFY.value])
            q = build_query_condition(self.request, q)
            items = tokenexchange_models.InvestInvite.objects.filter(q).order_by('-created_at')
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
                    item.kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show the te completed list:%s" % str(inst))
            return None


class AmountListView(generic.ListView):
    template_name = "newtonadmin/amount-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(AmountListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(AmountListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        context['form'] = forms_tokenexchange.AmountForm()
        context['token_exchange_info'] = settings.FUND_CONFIG[context['phase_id']]
        phase_id = settings.CURRENT_FUND_PHASE
        token_exchange_info = settings.FUND_CONFIG[phase_id]
        context['total_amount_btc'] = token_exchange_info["total_amount_btc"]
        context['total_amount_ela'] = token_exchange_info["total_amount_ela"]
        query_form = forms_tokenexchange.KYCQueryForm(initial=extract_query_parameter(self.request))
        context['query_form'] = query_form
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            q = Q(status=codes.TokenExchangeStatus.APPLY_AMOUNT.value, phase_id=phase_id)
            q = build_query_condition(self.request, q)
            items = tokenexchange_models.InvestInvite.objects.filter(q).order_by('-level')
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
                    item.kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show the amount list:%s" % str(inst))
            return None

class ConfirmListView(generic.ListView):
    template_name = "newtonadmin/amount-list.html"
    context_object_name = "items"
    paginate_by = 100
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(ConfirmListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(ConfirmListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        context['form'] = forms_tokenexchange.AmountForm()
        context['is_confirm'] = True
        context['token_exchange_info'] = settings.FUND_CONFIG[context['phase_id']]
        phase_id = settings.CURRENT_FUND_PHASE
        token_exchange_info = settings.FUND_CONFIG[phase_id]
        context['total_amount_btc'] = token_exchange_info["total_amount_btc"]
        context['total_amount_ela'] = token_exchange_info["total_amount_ela"]
        query_form = forms_tokenexchange.KYCQueryForm(initial=extract_query_parameter(self.request))
        context['query_form'] = query_form
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            q = Q(status=codes.TokenExchangeStatus.DISTRIBUTE_AMOUNT.value, phase_id=phase_id)
            q = build_query_condition(self.request, q)
            items = tokenexchange_models.InvestInvite.objects.filter(q).order_by('-level')
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
                    item.kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show the amount list:%s" % str(inst))
            return None

class CompletedAmountListView(generic.ListView):
    template_name = "newtonadmin/amount-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(CompletedAmountListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(CompletedAmountListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        context['form'] = forms_tokenexchange.AmountForm()
        context['is_completed'] = True
        query_form = forms_tokenexchange.KYCQueryForm(initial=extract_query_parameter(self.request))
        context['query_form'] = query_form
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            q = Q(status=codes.TokenExchangeStatus.CONFIRM_AMOUT.value, phase_id=phase_id)
            q = build_query_condition(self.request, q)
            items = tokenexchange_models.InvestInvite.objects.filter(q).order_by('-level')
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
                    item.kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show the te completed amount list:%s" % str(inst))
            return None


class ReceiveListView(generic.ListView):
    template_name = "newtonadmin/receive-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(ReceiveListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(ReceiveListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            items = tracker_models.AddressTransaction.objects.filter(phase_id=phase_id).order_by('-created_at')
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
                    item.kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show receive list:%s" % str(inst))
            return None


class UserReceiveListView(generic.ListView):
    template_name = "newtonadmin/user-receive-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(UserReceiveListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(UserReceiveListView, self).get_context_data(**kwargs)
        context['phase_id'] = int(self.request.path.split("/")[4])
        return context

    def get_queryset(self):
        try:
            phase_id = self.request.path.split("/")[4]
            phase_id = int(phase_id)
            items = []
            for item in tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id):
                queryset = tracker_models.AddressTransaction.objects.filter(user_id=item.user_id)
                btc_final_balance = queryset.filter(address=item.receive_btc_address, address_type=codes.CurrencyType.BTC.value).aggregate(Sum("value"))
                ela_final_balance = queryset.filter(address=item.receive_ela_address, address_type=codes.CurrencyType.ELA.value).aggregate(Sum("value"))
                btc_final_balance = btc_final_balance.get("value__sum")
                ela_final_balance = ela_final_balance.get("value__sum")
                if btc_final_balance and btc_final_balance != 0:
                    item.btc_value = btc_final_balance
                if ela_final_balance and ela_final_balance != 0:
                    item.ela_value = ela_final_balance
                if btc_final_balance and btc_final_balance != 0 or ela_final_balance and ela_final_balance !=0:
                    items.append(item)
            if items:
                for item in items:
                    item.user = User.objects.filter(id=item.user_id).first()
                    item.kycinfo = tokenexchange_models.KYCInfo.objects.filter(user_id=item.user_id).first()
            return items
        except Exception, inst:
            logger.exception("fail to show receive list:%s" % str(inst))
            return None


@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def confirm_id(request):
    """Confirm whether ID is valid
    
    """
    try:
        form = forms_tokenexchange.ConfirmKYCForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        user_id = int(form.cleaned_data['user_id'])
        pass_tokenexchange = int(form.cleaned_data['pass_kyc'])
        level = int(form.cleaned_data['level'])
        comment = form.cleaned_data['comment']
        item = tokenexchange_models.KYCInfo.objects.get(user_id=user_id, status=codes.KYCStatus.CANDIDATE.value)
        if pass_tokenexchange == 1:
            item.status = codes.KYCStatus.PASS_KYC.value
            item.level = level
            action_id = codes.AdminActionType.PASS_KYC.value
            is_pass = True
        elif pass_tokenexchange == 2:
            item.status = codes.KYCStatus.REJECT.value
            action_id = codes.AdminActionType.REJECT_KYC.value
            is_pass = False
        else:
            item.status = codes.KYCStatus.DENY.value
            action_id = codes.AdminActionType.DENY_KYC.value
            is_pass = False
        target_user = User.objects.filter(id=user_id).first()
        
        item.save()
        # add kyc audit
        kyc_audit = tokenexchange_models.KYCAudit(user_id=target_user.id,is_pass=is_pass,comment=comment)
        kyc_audit.save()
        # add audit log
        audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id,comment=comment)
        audit_log.save()
        # send the kyc pass notify
        item.kyc_audit = kyc_audit
        item.user = target_user
        is_send_success = services_tokenexchange.send_kycinfo_notify(item, request)
        if is_send_success:
            return http.JsonSuccessResponse()
        else:
            return http.JsonErrorResponse(error_message="send fail")
    except Exception, inst:
        logger.exception("fail to confirm id:%s" % str(inst))
        return http.JsonErrorResponse()        


@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def post_invite(request, phase_id):
    try:
        user_list = [int(item) for item in request.POST['user_list'].split(",")]
        for user_id in user_list:
            data = {"user_id":user_id}
            form = forms_tokenexchange.PostInviteForm(data)
            if not form.is_valid():
                return http.JsonErrorResponse()
            user_id = int(form.cleaned_data['user_id'])
            kyc_info = tokenexchange_models.KYCInfo.objects.get(user_id=user_id)
            invite = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user_id=user_id).first()
            if not invite:
                invite = tokenexchange_models.InvestInvite()
                invite.user_id = user_id
                invite.phase_id = int(phase_id)
            invite.status = codes.TokenExchangeStatus.INVITE.value
            # copy fields to invite table for query
            invite.kyc_type = kyc_info.kyc_type
            invite.level = kyc_info.level
            invite.is_establish_node = kyc_info.is_establish_node
            invite.country = kyc_info.country
            invite.save()
            action_id = codes.AdminActionType.INVITE.value
            target_user = User.objects.filter(id=user_id).first()
            audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id)
            audit_log.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to post invite:%s" % str(inst))
        return http.JsonErrorResponse()


@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def send_invite_email(request, phase_id):
    try:
        user_list = [int(item) for item in request.POST['user_list'].split(",")]
        for user_id in user_list:
            data = {"user_id":user_id}
            form = forms_tokenexchange.PostInviteForm(data)
            if not form.is_valid():
                return http.JsonErrorResponse()
            user_id = int(form.cleaned_data['user_id'])
            target_user = User.objects.filter(id=user_id).first()
            phase_id = int(phase_id)
            invite = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user_id=user_id).first()
            if not invite:
                return http.JsonErrorResponse()
            kyc_info = tokenexchange_models.KYCInfo.objects.filter(user_id=user_id).first()
            invite.kyc_info = kyc_info
            invite.tokenexchange_info = settings.FUND_CONFIG[invite.phase_id]
            invite.user = target_user
            if not services_tokenexchange.send_apply_amount_notify(invite, request):
                return http.JsonErrorResponse(error_message="send fail")
            else:
                invite.status = codes.TokenExchangeStatus.SEND_INVITE_NOTIFY.value
                invite.save()
            action_id = codes.AdminActionType.SEND_INVITE.value
            audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id)
            audit_log.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to send the invite email:%s" % str(inst))
        return http.JsonErrorResponse()


@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def post_amount(request, phase_id):
    """submit the distribution amount
    
    """
    try:
        form = forms_tokenexchange.AmountForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse()
        phase_id = int(phase_id)
        user_id = int(form.cleaned_data['user_id'])
        assign_btc = int(form.cleaned_data['assign_btc'])
        assign_ela = int(form.cleaned_data['assign_ela'])
        # Query the available address
        if assign_btc != 0:
            btc_address = services_tokenexchange.allocate_btc_address()
        else:
            btc_address = None
        if assign_ela == 0:
            ela_address = None
        else:
            ela_address = services_tokenexchange.allocate_ela_address()
        if not btc_address and not ela_address:
            return http.JsonErrorResponse()
        # save status
        item = tokenexchange_models.InvestInvite.objects.filter(user_id=user_id, phase_id=phase_id).first()
        if item.status == codes.TokenExchangeStatus.APPLY_AMOUNT.value:
            item.status = codes.TokenExchangeStatus.DISTRIBUTE_AMOUNT.value
            item.assign_ela = assign_ela
            item.assign_btc = assign_btc
            item.receive_btc_address = btc_address
            item.receive_ela_address = ela_address
            item.save()
            action_id = codes.AdminActionType.ASSIGN_AMOUNT.value
            target_user = User.objects.filter(id=user_id).first()
            audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id)
            audit_log.save()
        elif item.status == codes.TokenExchangeStatus.DISTRIBUTE_AMOUNT.value:
            item.status = codes.TokenExchangeStatus.CONFIRM_AMOUT.value
            item.assign_ela = assign_ela
            item.assign_btc = assign_btc
            item.receive_btc_address = btc_address
            item.receive_ela_address = ela_address
            item.save()
            action_id = codes.AdminActionType.CONFIRM_AMOUNT.value
            target_user = User.objects.filter(id=user_id).first()
            audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id)
            audit_log.save()
            
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to post amount:%s" % str(inst))
        return http.JsonErrorResponse()



@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def send_receive_email(request, phase_id):
    """Send email to investor for notifing them that we have recevied coin.
    """
    try:
        phase_id = int(phase_id)
        user_list = [int(item) for item in request.POST['user_list'].split(",")]
        for user_id in user_list:
            item = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user_id=user_id).first()
            user = User.objects.filter(id=item.user_id).first()
            item.user = user
            kyc_info = tokenexchange_models.KYCInfo.objects.filter(user_id=user_id).first()
            queryset = tracker_models.AddressTransaction.objects.filter(phase_id=phase_id, user_id=user_id)
            btc_set = queryset.filter(address=item.receive_btc_address, address_type=codes.CurrencyType.BTC.value)
            ela_set = queryset.filter(address=item.receive_ela_address, address_type=codes.CurrencyType.ELA.value)
            btc_final_balance = 0
            ela_final_balance = 0
            if btc_set:
                for item_btc in btc_set:
                    btc_final_balance = btc_final_balance + item_btc.value
            if ela_set:
                for item_ela in ela_set:
                    ela_final_balance = ela_final_balance + item_ela.value
            if btc_final_balance != 0:
                item.btc_value = btc_final_balance
            if ela_final_balance != 0:
                item.ela_value = ela_final_balance
            item.kyc_info = kyc_info
            if services_tokenexchange.send_receive_confirm_notify(request, item):
                item.status = codes.TokenExchangeStatus.SEND_RECEIVE_AMOUNT_NOTIFY.value
                item.save()
                action_id = codes.AdminActionType.SEND_CONFIRM_EMAIL.value
                target_user = User.objects.filter(id=item.user_id).first()
                audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id)
                audit_log.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to post email to investor:%s" % str(inst))
        return http.JsonErrorResponse()


@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def show_id_detail(request, user_id):
    """show detail info
    """
    try:
        item = tokenexchange_models.KYCInfo.objects.filter(user_id=user_id).first()
        if item:
            if item.id_type:
                item.id_type = convert.get_value_from_choice(item.id_type, tokenexchange_models.ID_CHOICES)
            if item.is_establish_node:
                item.is_establish_node = convert.get_value_from_choice(item.is_establish_node, tokenexchange_models.ESTABLISH_CHOICE)
            if item.which_node_establish:
                item.which_node_establish = convert.get_value_from_choice(item.which_node_establish, tokenexchange_models.NODE_CHOICE)
            item.country = COUNTRIES[item.country]
            item.level_choices = [i+1 for i in range(10)]
        return render(request, "newtonadmin/id-detail.html", locals())
    except Exception, inst:
        logger.exception("fail to post email to investor:%s" % str(inst))
        return http.JsonErrorResponse()


class RejectListView(generic.ListView):
    """reject id list
    """
    template_name = "newtonadmin/id-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(RejectListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(RejectListView, self).get_context_data(**kwargs)
        context['countries_choices'] = COUNTRIES
        context['title'] = '已驳回'
        return context

    def get_queryset(self):
        try:
            items = []
            fields = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.REJECT.value)
            if fields and len(fields) > 0:
                for item in fields:
                    if item.id_type:
                        item.id_type = convert.get_value_from_choice(item.id_type, tokenexchange_models.ID_CHOICES)
                    item.country = COUNTRIES[item.country]
                    items.append(item)
            return items
        except Exception, inst:
            logger.exception("fail to show pass id list:%s" % str(inst))
            return None

class DenyListView(generic.ListView):
    """reject id list
    """
    template_name = "newtonadmin/id-list.html"
    context_object_name = "items"
    paginate_by = settings.PAGE_SIZE
    
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            response = super(DenyListView, self).get(request, *args, **kwargs)
            return response
        else:
            return redirect("/newtonadmin/login/")

    def get_context_data(self, **kwargs):
        context = super(DenyListView, self).get_context_data(**kwargs)
        context['title'] = '已拒绝'
        return context

    def get_queryset(self):
        try:
            items = []
            fields = tokenexchange_models.KYCInfo.objects.filter(status=codes.KYCStatus.DENY.value)
            if fields and len(fields) > 0:
                for item in fields:
                    if item.id_type:
                        item.id_type = convert.get_value_from_choice(item.id_type, tokenexchange_models.ID_CHOICES)
                    item.country = COUNTRIES[item.country]
                    items.append(item)
            return items
        except Exception, inst:
            logger.exception("fail to show pass id list:%s" % str(inst))
            return None

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def post_confirm_amount(request, phase_id):
    """confirm assign amount
    """
    try:
        user_list = [int(item) for item in request.POST['user_list'].split(",")]
        for user_id in user_list:
            data = {"user_id":user_id}
            form = forms_tokenexchange.PostInviteForm(data)
            if not form.is_valid():
                return http.JsonErrorResponse()
            user_id = int(form.cleaned_data['user_id'])
            invite = tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id, user_id=user_id).first()
            if not invite:
                invite = tokenexchange_models.InvestInvite()
                invite.user_id = user_id
                invite.phase_id = int(phase_id)
            invite.status = codes.TokenExchangeStatus.CONFIRM_AMOUT.value
            invite.save()
            action_id = codes.AdminActionType.CONFIRM_AMOUNT.value
            target_user = User.objects.filter(id=user_id).first()
            audit_log = newtonadmin_models.AuditLog(user=request.user,target_user=target_user,action_id=action_id)
            audit_log.save()
        return http.JsonSuccessResponse()
    except Exception, inst:
        logger.exception("fail to post invite:%s" % str(inst))
        return http.JsonErrorResponse()

@user_passes_test(lambda u: u.is_staff, login_url='/newtonadmin/login/')
def export_amount_list(request, phase_id):
    """Export the amount list as csv format
    """
    try:
        response = http.HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="amount-list.csv"'
        writer = csv.writer(response)
        writer.writerow([u'邮箱', u'申请BTC数量', u'分配BTC数量', u'申请ELA数量', u'分配ELA数量'])
        for item in tokenexchange_models.InvestInvite.objects.filter(phase_id=phase_id):
            user = User.objects.get(id=item.user_id)
            email = user.email
            writer.writerow([email, item.expect_btc, item.assign_btc, item.expect_ela, item.assign_ela])
        return response
    except Exception, inst:
        logger.exception("fail to export amount list:%s" % str(inst))
        raise exception.SystemError500()
        
