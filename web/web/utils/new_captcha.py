# -*- coding: utf-8 -*-
import logging
from captcha.image import ImageCaptcha

logger = logging.getLogger(__name__)

def generate_captcha_image(code):
    """Generate the captcha image by the code
    """
    try:
        image = ImageCaptcha()
        data = image.generate(code)
        return data
    except Exception, inst:
        logger.exception("fail to generate the captcha image:%s" % str(inst))
        return None
