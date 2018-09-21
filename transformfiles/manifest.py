import collections
import datetime
import textwrap

from django.conf import settings
from django.contrib.staticfiles.finders import get_finder
from django.utils.functional import cached_property
from transformfiles.transforms import get_registry
import sass


TransformfilesManifestEntry = collections.namedtuple(
    'TransformfilesManifestEntry', ['build', 'src', 'transforms'])


class TransformfilesManifestSource:
    def __init__(self, path, storage):
        self.path = path
        self.storage = storage

    @cached_property
    def abspath(self):
        return self.storage.path(self.path)


class TransformfilesManifest:
    """Singleton data object that holds parsed configuration values based on
    settings.TRANSFORMFILES_MANIFEST"""

    def __init__(self, raw, ignore_patterns=''):
        self.ignore_patterns = ignore_patterns
        self.registry = get_registry()
        self.manifest = {}
        for entry in raw:
            key, entry = self._build_entry(entry)
            self.manifest[key] = entry

    def find(self, key):
        return self.manifest[key]

    def items(self):
        for key, value in self.manifest.items():
            yield value

    def _build_entry(self, raw_entry):
        buildpath = raw_entry[0]

        raw_srcpath = raw_entry[1]
        srcpath = self._build_srcpath(raw_srcpath)

        transform_ids = raw_entry[2]
        if isinstance(transform_ids, str):
            transform_ids = [transform_ids]

        transforms = []
        for tid in transform_ids:
            transform = self.registry.get(tid)
            transforms.append(transform)

        return buildpath, TransformfilesManifestEntry(
            build=buildpath, src=srcpath, transforms=transforms)

    def _build_srcpath(self, srcpath):
        for finder in get_src_finders():
            for path, storage in finder.list(self.ignore_patterns):
                if srcpath == path:
                    return TransformfilesManifestSource(path=path, storage=storage)

        raise MissingSourceFileException(
            "Source file '{}' does not exist".format(srcpath))


class MissingSourceFileException(Exception):
    pass


def get_src_finders():
    for finder_path in settings.STATICFILES_FINDERS:
        if not finder_path.endswith("TransformfilesFinder"):
            yield get_finder(finder_path)


transformfiles_manifest = TransformfilesManifest(raw=settings.TRANSFORMFILES_MANIFEST)
