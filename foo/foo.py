import sys

from django.conf import settings
import os

DEBUG = os.environ.get("DEBUG", 'on')
SECRET_KEY = os.environ.get("SECRET_KEY", 'd0*p8*gtndjq-jsv6l&64+-qtncc1081!8@y24#e^gl9kuahhl')
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    )
)

from django.conf.urls import url
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World")


urlpatterns = (
    url(r'^$', index),
)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
