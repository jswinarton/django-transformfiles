import collections
import datetime
import textwrap

from django.conf import settings
from django.contrib.staticfiles.finders import get_finder
from django.utils.functional import cached_property
from transformfiles.transforms import get_registry


class ManifestEntry:
    def __init__(self, build_path, src_path, src_storage, transforms):
        self.build_path = build_path
        self.src_path = src_path
        self.src_storage = src_storage
        self.transforms = transforms

    # @cached_property
    # def src_abspath(self):
    #     return self.src_storage.path(self.src_path)

    def modified_time(self):
        return self.src_storage.get_modified_time(self.src_path)


class Manifest:
    """Singleton data object that holds parsed configuration values based on
    settings.TRANSFORMFILES_MANIFEST"""

    def __init__(self, raw, ignore_patterns=''):
        self.ignore_patterns = ignore_patterns
        self.registry = get_registry()
        self.manifest = {}
        self.src_finders = self._get_src_finders()

        for entry in raw:
            key, entry = self._build_entry(entry)
            self.manifest[key] = entry

    def find(self, key):
        return self.manifest.get(key)

    def items(self):
        return self.manifest.items()

    def _build_entry(self, raw_entry):
        build_path, raw_src_path, transform_ids = raw_entry

        src_path, src_storage = self._build_srcpath(raw_src_path)

        if isinstance(transform_ids, str):
            transform_ids = [transform_ids]

        transforms = []
        # iterate backwards, so transforms acts like a stack
        for tid in reversed(transform_ids):
            transform = self.registry.get(tid)
            transforms.append(transform)

        return build_path, ManifestEntry(
            build_path=build_path, src_path=src_path,
            src_storage=src_storage, transforms=transforms)

    def _build_srcpath(self, srcpath):
        for finder in self.src_finders:
            for path, storage in finder.list(self.ignore_patterns):
                if srcpath == path:
                    return path, storage

        raise MissingSourceFileException(
            "Source file '{}' does not exist".format(srcpath))

    def _get_src_finders(self):
        src_finders = []
        for finder_path in settings.STATICFILES_FINDERS:
            if not finder_path.endswith("TransformfilesFinder"):
                finder = get_finder(finder_path)
                src_finders.append(finder)
        return src_finders


# TODO move this to finders class
def get_src_finders():
    src_finders = []
    for finder_path in settings.STATICFILES_FINDERS:
        if not finder_path.endswith("TransformfilesFinder"):
            finder = get_finder(finder_path)
            src_finders.append(finder)
    return src_finders


def get_src_storages(raw_entries):
    search_paths = set()
    paths_with_storages = []

    for _build_path, src_path, _transforms in raw_entries:
        search_paths.add(src_path)

    for finder in get_src_finders():
        for path, storage in finder.list(ignore_patterns=''):
            if not search_paths:
                return None
            if path in search_paths:
                search_paths.remove(path)
                yield (path, storage)


class MissingSourceFileException(Exception):
    pass


# transformfiles_manifest = TransformfilesManifest(raw=settings.TRANSFORMFILES_MANIFEST)
