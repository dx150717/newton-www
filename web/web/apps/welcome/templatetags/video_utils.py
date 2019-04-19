# -*- coding: utf-8 -*-
import re
import logging
from django import template
from django.template import Context, loader
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

__author__ = ''
__version__ = '$Rev$'
__doc__ = """ """

logger = logging.getLogger(__name__)
register = template.Library()


class VideoItem(object):
    def __init__(self, title, summary, poster, url, display='display:none;'):
        self.title = title
        self.summary = summary
        self.poster = poster
        self.url = url
        self.display = display


class ShowHomepageVideoNode(template.Node):
    def __init__(self):
        pass

    """
    https://newton-video.oss-cn-beijing.aliyuncs.com/EP1NewPhilosophy.mp4
    https://newton-video.oss-cn-beijing.aliyuncs.com/EP2NewBlockchain.mp4
    https://newton-video.oss-cn-beijing.aliyuncs.com/EP3NewEcosystem.mp4
    https://newton-video.oss-cn-beijing.aliyuncs.com/EP4NewCoin.mp4
    
    """
    def render(self, context):
        request = context['request']
        template = loader.get_template('welcome/include-video.html')
        videos = [
            #1
            VideoItem(
                _(u"The Tech Behind Newton"),
                _(u"What is Newton's Key Tech"),
                '%simages/meeting/videos/new-tech.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/EP5Newtech.mp4',display=''),
            #2
            VideoItem(
                _(u"New Blockchain"),
                _(u"How does Newton use the Blockchain?"),
                '%simages/meeting/videos/new-tech.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/EP2NewBlockchain.mp4'
            ),
            #3
            VideoItem(
                _(u"New Ecosystem"),
                _(u"How to build this Ecosystem?"),
                '%simages/meeting/videos/new-tech.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/EP3NewEcosystem.mp4'
            ),
            #4
            #VideoItem(
            #    _(u"NEW Token"),
            #    _(u"What are the utilities of NEW Token?"),
            #    '%simages/meeting/videos/new-tech.jpg' % settings.STATIC_URL,
            #    'https://newton-video.oss-cn-beijing.aliyuncs.com/EP4NewCoin.mp4'
            #),
            #5
            VideoItem(
                _(u"New Philosophy"),
                _(u"How can we upgrade the economy?"),
                '%simages/meeting/videos/new-tech.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/EP1NewPhilosophy.mp4'
            ),
            #6
            VideoItem(
                _(u"2018 Newton Community Node Conference"),
                _(u"On December 11, 2018, Newton held its first community node conference at the MGM Cotai, Macao."),
                '%simages/meeting/videos/A.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/macao-2019-a.mp4'
            ),
            #7
            VideoItem(
                _(u"What is Newton"),
                _(u"Newton: Infrastructure for the Community Economy"),
                '%simages/whats-newton.jpeg' % settings.STATIC_URL,
                'https://www.newtonproject.org/filestorage/uploads/newton-introduction.mp4'),
        ]
        #You need manual specific the video_sum for high performance
        video_sum = len(videos)
        context = RequestContext(request, locals())
        html = template.render(context)
        return html


class ShowNewPayVideoNode(template.Node):
    def __init__(self):
        pass
    def render(self, context):
        request = context['request']
        template = loader.get_template('welcome/newpay_video.html')
        videos = [
            # 1
            VideoItem(
                _(u"All About NewForce And How to Earn NEW"),
                _(u"NewForce Introduction"),
                '%simages/newpay/videos/All_About_NewForce_and_how_to_earn_NEW.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/newpayintro/All_About_NewForce_and_how_to_earn_NEW.mp4', display=''),
            # 2
            VideoItem(
                _(u"How To Keep Newton's NewPay Wallet Safe?"),
                _(u"Keep your Mnemonic Phrase safe"),
                '%simages/newpay/videos/How_to_Keep_Newtons_NewPay_Wallet_Safe.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/newpayintro/How_to_Keep_Newtons_NewPay_Wallet_Safe.mp4'),

            # 3 Attention Plz, This is Multi Language!
            VideoItem(
                _(u"How To Use NewPay To Earn Money"),
                _(u"NewPay App Tutorial"),
                '%simages/newpay/videos/How_to_use_NewPay_to_Earn_Money.jpg' % settings.STATIC_URL,
                _('https://newton-video.oss-cn-beijing.aliyuncs.com/newpayintro/How_to_use_NewPay_to_Earn_Money.mp4')),

            # 4
            VideoItem(
                _(u"Only Crypto Wallet You May Need In the Future"),
                _(u"Crypto Strategy"),
                '%simages/newpay/videos/Only_Crypto_Wallet_You_May_Need_in_the_Future.jpg' % settings.STATIC_URL,
                'https://newton-video.oss-cn-beijing.aliyuncs.com/newpayintro/Only_Crypto_Wallet_You_May_Need_in_the_Future.mp4')
        ]
        # You need manual specific the video_sum for high performance
        video_sum = len(videos)
        context = RequestContext(request, locals())
        html = template.render(context)
        return html

@register.tag(name='show_homepage_video')
def show_homepage_video(parser, token):
    return ShowHomepageVideoNode()

@register.tag(name='show_newpay_video')
def show_newpay_video(parser, token):
    return ShowNewPayVideoNode()

