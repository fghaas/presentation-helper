from .generic import PresentationCreator as GenericPresentationCreator

from .generic import IndexRenderer as GenericIndexRenderer

from jinja2 import Environment, PackageLoader


class RevealIndexRenderer(GenericIndexRenderer):

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

    def _setup_template(self, template_path=None):
        env = Environment(loader=PackageLoader('presentationhelper',
                                               'templates'),
                          trim_blocks=True,
                          lstrip_blocks=True)
        self.template = env.get_template('reveal/index.html.j2')


class RevealPresentationCreator(GenericPresentationCreator):

    INDEX_RENDERER_CLASS = RevealIndexRenderer
