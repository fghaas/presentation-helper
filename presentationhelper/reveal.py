# -*- coding: utf-8 -*-
from .generic import PresentationCreator as GenericPresentationCreator

from .generic import TemplateRenderer as GenericTemplateRenderer

from jinja2 import FileSystemLoader, PackageLoader

import os


class RevealTemplateRenderer(GenericTemplateRenderer):

    DEFAULTS = {
        'theme': 'white',
        'highlight': 'github',
        'controls': {
            'enable': True,
            'tutorial': True,
            'layout': 'bottom-right',
            'back_arrows': 'faded',
        },
        'progress': True,
        'show_notes': False,
        'markdown': {
            'path': 'markdown',
            'separator': '^\\n\\n\\n',
            'separator-vertical': '^\\n\\n',
            'separator-notes': '^Note:',
        },
        'sections': [],
    }

    def _setup_loaders(self):
        super(RevealTemplateRenderer, self)._setup_loaders()
        loader = None
        if __file__ == os.path.abspath(__file__):
            # We're on Python 3.4 and later. __file__ is an absolute
            # path, we can use PackageLoader.
            loader = PackageLoader('presentationhelper',
                                   os.path.join('templates', 'reveal'))
        else:
            # __file__ is a relative path, PackageLoader won't
            # work. Use a FileSystemLoader instead.
            module_path = os.path.dirname(os.path.abspath(__file__))
            loader = FileSystemLoader(os.path.join(module_path,
                                                   'templates',
                                                   'reveal'))
        self.loaders.append(loader)


class RevealPresentationCreator(GenericPresentationCreator):

    TEMPLATE_RENDERER_CLASS = RevealTemplateRenderer
