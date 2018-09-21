import datetime
import importlib

from django.conf import settings


def build_stamp(outfile, infile, **kwargs):
    date = datetime.date.today().strftime('%Y-%m-%d')
    footer = "\n\n/* Built on {} */\n".format(date)
    outfile.write(infile.read())
    outfile.write(footer)


class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, *args, **kwargs):
        def wrapped(func):
            name = kwargs.get('name') or func.__name__
            namespace = kwargs.get('namespace')
            if namespace is not None:
                name = "{namespace}.{name}".format(
                    namespace=namespace, name=name)
            self._registry[name] = func
            return func

        if len(args) == 1 and callable(args[0]):
            return wrapped(args[0])

        return wrapped

    def get(self, key):
        try:
            return self._registry[key]
        except KeyError:
            raise Exception("transform '{}' not found in registry".format(key))

    def items(self):
        return self._registry.items()

    def add_registry(self, registry):
        self._registry.update(registry._registry)


def get_registry():
    master_registry = Registry()
    master_registry.register(build_stamp)

    for module in getattr(settings, 'TRANSFORMFILES_REGISTRY_MODULES', []):
        module = importlib.import_module(module)
        master_registry.add_registry(module.registry)

    return master_registry
