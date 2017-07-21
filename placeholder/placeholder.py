import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
import os

DEBUG = os.environ.get("DEBUG", 'on')
SECRET_KEY = os.environ.get(
    "SECRET_KEY", 'gj6lf!)$*2ycr4i#dwkj&cir!ljfe$p47^-$s7zi^l@9svivuf')
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


def placeholder(request, width, height):
    return HttpResponse("OK")


def index(request):
    return HttpResponse("Hello World")


urlpatterns = (
    url(r'^$', index, name="homepage"),
    url(r'^image/(?P<width>\d+)x(?P<height>\d+)/$',
        placeholder, name="placeholder")
)

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

from django import forms


class ImageForm():
    """
    form to validate requested placeholder image.
    """

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)
