from . import IndexRenderer

from jinja2 import Environment, PackageLoader


class RevealIndexRenderer(IndexRenderer):

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

    def _update_template(self, template):
        if template:
            self.template = template
        else:
            env = Environment(loader=PackageLoader('presentationhelper',
                                                   'templates'),
                              trim_blocks=True,
                              lstrip_blocks=True)
            self.template = env.get_template('reveal/index.html.j2')
