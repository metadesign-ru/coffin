# -*- coding: utf-8 -*-
"""
A Django template loader wrapper for Coffin that intercepts
requests for "*.jinja" templates, rendering them with Coffin
instead of Django templates.

Usage:

TEMPLATE_LOADERS = (
    'coffin.contrib.loader.AppLoader',
    'coffin.contrib.loader.FileSystemLoader',
)

"""

from os.path import splitext
from django.conf import settings
from django.template.loaders import app_directories, filesystem
from coffin.template.loader import get_template


JINJA2_DEFAULT_TEMPLATE_EXTENSION = getattr(settings,
    'JINJA2_DEFAULT_TEMPLATE_EXTENSION', ('.jinja',))

if isinstance(JINJA2_DEFAULT_TEMPLATE_EXTENSION, basestring):
    JINJA2_DEFAULT_TEMPLATE_EXTENSION = (JINJA2_DEFAULT_TEMPLATE_EXTENSION,)


class LoaderMixin(object):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        extension = splitext(template_name)[1]

        if not extension in JINJA2_DEFAULT_TEMPLATE_EXTENSION:
            return super(LoaderMixin, self).load_template(template_name,
                template_dirs)
        template = get_template(template_name)
        return template, template.filename


class FileSystemLoader(LoaderMixin, filesystem.Loader):
    pass


class AppLoader(LoaderMixin, app_directories.Loader):
    pass
