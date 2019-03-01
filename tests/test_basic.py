import os

from django.conf import settings
# from transformfiles.finders import TransformfilesFinder
from transformfiles.manifest import Manifest, ManifestEntry, get_src_finders, get_src_storages
import pytest


@pytest.fixture
def manifest():
    return Manifest([
        ("build.css", "sample.css", []),
    ])


def test_basic(manifest):
    assert isinstance(manifest.find("build.css"), ManifestEntry)


def test_get_src_finders_not_contains_transformfiles_finder():
    finders = get_src_finders()
    for finder in finders:
        assert not isinstance(finder, TransformfilesFinder)


def test_get_src_storages():
    raw_entries = [
        ("build.css", "sample.css", []),
    ]
    assert False
    for path, storage in get_src_storages(raw_entries):
        assert path, storage == False
