from django.contrib.staticfiles.finders import BaseFinder
from django.conf import settings
from transformfiles.manifest import transformfiles_manifest
from transformfiles.storage import transformfiles_storage


class TransformfilesFinder(BaseFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find(self, path, all=False):
        # TODO handle properly if all=True, or at least document why it's not
        # relevant here
        path = transformfiles_manifest.find(path).build
        transformfiles_storage.compile(path)
        return transformfiles_storage.path(path)

    def list(self, ignore_patterns):
        # TODO deal with ignore_patterns sensibly
        for entry in transformfiles_manifest.items():
            yield entry.build, transformfiles_storage
