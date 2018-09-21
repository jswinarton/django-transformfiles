import collections
import io
import os
import tempfile

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import sass

from transformfiles.manifest import transformfiles_manifest


class OperationNotAllowed(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args or ("This operation is not allowed on this storage class",)


class TransformfilesStorage(FileSystemStorage):
    """A storage class that manages the storage and retrieval of build files

    Calls to basic read operations will return the compiled file, compiling
    it if it does not exist or is out of date. The class also includes utility
    functions for handling the compile process manually.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        # keep a reference available to the temp directory so it is not
        # garbage collected until this class is destroyed
        self.tmpdir = tempfile.TemporaryDirectory()

        if location is None:
            location = self.tmpdir.name
        if base_url is None:
            base_url = settings.STATIC_URL

        super().__init__(location, base_url, *args, **kwargs)

    def compile(self, path, force=False):
        """Compile the file at path from its source files and transforms

        Passing force=True will compile the file regardless of its modification
        time.
        """
        if force or self.is_stale(path):
            self._compile(path)
        return self.path(path)

    def _compile(self, path):
        config = transformfiles_manifest.find(path)
        buildpath = self.path(path)

        basedir = os.path.dirname(buildpath)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        # TODO support multiple input files
        src = config.src
        bufin = src.storage.open(src.path, 'r')

        transforms = collections.deque(config.transforms)
        while transforms:
            bufout = io.StringIO()
            kwargs = {
                'remaining_transforms': transforms,
                'config': config,
            }

            t = transforms.popleft()
            t(bufout, bufin, **kwargs)

            bufin.close()
            bufin = bufout
            bufin.seek(0)

        with open(buildpath, 'w') as buildfile:
            buildfile.write(bufin.read())
            bufin.close()

        return buildpath

    def open(self, path):
        self.compile(path)
        return super().open(path)

    def exists(self, path):
        """Determines if path exists in the manifest"""
        try:
            transform_manifest.find(path)
            return True
        except KeyError:
            return False

    def get_modified_time(self, path):
        """Get the last modified time of the source file

        Returns the last modified time of source file that was modified last.
        This allows management tools like collectstatic to know when to recopy
        the files to STATIC_ROOT.
        """
        config = transformfiles_manifest.find(path)
        src = config.src
        return src.storage.get_modified_time(src.path)

    def is_stale(self, path):
        """Determines if the file at path is out of date

        The file is out of date if the source file has been modified
        after the last compilation.
        """
        if not self._fs_exists(path):
            return True

        src_mtime = self.get_modified_time(path)
        build_mtime = self._fs_get_modified_time(path)

        return build_mtime < src_mtime

    def _fs_exists(self, path):
        """Determines if the path exists in the filesystem"""
        return super().exists(path)

    def _fs_get_modified_time(self, path):
        """Gets the last modified time of the build artifact"""
        return super().get_modified_time(path)

    def delete(self, *args, **kwargs):
        raise OperationNotAllowed

    def save(self, *args, **kwargs):
        raise OperationNotAllowed


transformfiles_storage = TransformfilesStorage()
