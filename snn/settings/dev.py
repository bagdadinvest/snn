from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "yemc*^mx)tzc4%m%=tt--j#hr6%-imw+evx_k2u@mq**)r2k4j"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WAGTAIL_CACHE = False

try:
    from .local import *  # noqa
except ImportError:
    pass

CSRF_TRUSTED_ORIGINS = ['https://salonnassnor.com']
