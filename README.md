# django-transformfiles

Modern, simple and flexible asset pipeline manager for Django.

django-transformfiles is designed to integrate as seamlessly as possible into a
Django app, with no obtuse configuration properties or changes to template
files. Everything "just works."

- Easy to configure and use; template libraries are drop-in replacements for existing Django libraries
- They're just staticfiles, they shouldn't be treated any differently from
  other files. No extra configuration for s3 for example. No extra commands,
  just run collectstatic
- Complete control over where they end up
- Webpack-style configuration in settings
- Simple, modular transformations
- Define your own transformations


## Installation

Install the `transformfiles` package with pip:

```
$ pip install transformfiles
```

Add `transformfiles` to `INSTALLED_APPS` and add the finder to `STATICFILES_FINDERS`:

```python
INSTALLED_APPS = [
  # ...
  'transformfiles',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'transformfiles.finders.TransformfilesFinder',
]
```

## Usage

File transformation flows are defined using a manifest. The manifest can be
defined as a JSON or YAML document, or it can be defined directly in the
settings file.

### Document-based manifest

`settings.py`:

```python
TRANSFORMFILES_MANIFEST = 'config/transformfiles_manifest.yml'
```

`transformfiles_manifest.yml`:
```yaml
---
- target: css/build.css
  source: scss/main.scss
  transforms:
    - scss.build
    - build_stamp
```


### Settings-based manifest

```python
TRANSFORMFILES_MANIFEST = [
    ("css/build.css", "scss/main.scss", ["scss.build", "build_stamp"]),
]
```

## Defining transformations

django-transformfiles ships with a handful of useful transformations out of the
box. It is also simple to define your own using a function. Here is a sample
transformation that adds a timestamp to the end of the output file:

```python
def build_stamp(outfile, infile, **kwargs):
    date = datetime.date.today().strftime('%Y-%m-%d')
    footer = "\n\n/* Built on {} */\n".format(date)
    outfile.write(infile.read())
    outfile.write(footer)
```

## Cache invalidation

django-transformfiles includes support for cache busting by changing the
filenames of files when they are recompiled. Cache busting is off by default.
To turn it on, apply the following setting:

```python
TRANSFORMFILES_CACHE_INVALIDATION = True
```



## TODO

- [ ] Rewrite compiler library as a standalone class without backing FileSystemStorage
- [ ] Allow specification of manifest in JSON/YAML
- [ ] Support for cache-busting, or docs on how to integrate with Django ManifestStaticFilesStorage
- [ ] Support concatenation of multiple files into one
- [ ] Support file-dependency mtime overrides (e.g. SCSS files import other files during compilation; the whole file should compile if a subfile is changed)
