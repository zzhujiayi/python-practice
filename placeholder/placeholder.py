import sys
from django.conf import settings
from django.core.wsgi import get_wsgi_application
import os
from django.conf.urls import url
from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.cache import cache
from django.views.decorators.http import etag
import hashlib
from django.core.urlresolvers import reverse
from django.shortcuts import render

DEBUG = os.environ.get("DEBUG", 'on')
SECRET_KEY = os.environ.get(
    "SECRET_KEY", 'gj6lf!)$*2ycr4i#dwkj&cir!ljfe$p47^-$s7zi^l@9svivuf')
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
    ),
    TEMPLATES=(
        {
            'BAKEND': 'django.template.bakends.django.DjangoTemplates',
            'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        },
    ),
    STATICFILES_DIR=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
)


class ImageForm(forms.Form):
    """
    form to validate requested placeholder image.
    """

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        width = forms.cleaned_data['width']
        height = forms.cleaned_data['height']
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)
        return content


def generate_etag(request, width, height):
    content = 'Placeholder: {0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')
    return HttpResponse("OK")


def index(request):
    example = reverse('placeholder', kwargs={'width': 50, 'height': 50})
    context = {
        'example': request.build_absolute_url(example)
    }

    return render(request, 'home.html', context)


urlpatterns = (
    url(r'^$', index, name="homepage"),
    url(r'^image/(?P<width>\d+)x(?P<height>\d+)/$',
        placeholder, name="placeholder")
)

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)