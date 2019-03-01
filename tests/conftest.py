import os

import django
from django.conf import settings


def pytest_configure():
    tests_dir=os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        BASE_DIR=tests_dir,
        INSTALLED_APPS=['transformfiles'],
        STATICFILES_FNDERS=[
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            'transformfiles.finders.TransformfilesFinder',
        ],
        STATICFILES_DIRS=[
            os.path.join(tests_dir, 'static')
        ]

    )
    django.setup()
