import os

from django.conf import settings
import sass
from transformfiles import transforms


registry = transforms.Registry()


@registry.register(namespace='scss')
def build(outfile, infile, **kwargs):
    build_development = getattr(
        settings, 'TRANSFORMFILES_SCSS_BUILD_DEVELOPMENT', settings.DEBUG)

    abspath = kwargs['config'].src.abspath
    srcdir = os.path.dirname(abspath)

    extra_settings = {'include_paths': [srcdir]}
    if not build_development:
        extra_settings.update({'output_style': 'compressed'})

    out = sass.compile(
        string=infile.read(), **extra_settings)
    outfile.write(out)
