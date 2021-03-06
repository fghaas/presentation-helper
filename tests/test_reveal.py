# -*- coding: utf-8 -*-
import csv
from io import StringIO
import os
import shutil
import tempfile
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET
import yaml

from unittest import TestCase

import presentationhelper
from presentationhelper.reveal import RevealPresentationCreator
from presentationhelper.reveal import RevealConfig


NSMAP = {'xhtml': 'http://www.w3.org/1999/xhtml'}

DIR = os.path.dirname(os.path.realpath(__file__))
MODULE_DIR = os.path.dirname(presentationhelper.__file__)


class ConfigTestCase(TestCase):

    def test_str(self):
        config = RevealConfig()
        config_str = str(config)
        stream = StringIO(config_str)
        d = yaml.safe_load(stream)
        self.assertIn('theme', d.keys())

    def test_default_config(self):
        config = RevealConfig()
        self.assertEqual(config.to_dict(), {
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
        })

    def test_default_config_writeback(self):
        config = RevealConfig()
        with NamedTemporaryFile(mode='w') as writer:
            config.dump(writer)
            with open(writer.name, 'r') as reader:
                expected = """controls:
  back_arrows: faded
  enable: true
  layout: bottom-right
  tutorial: true
highlight: github
markdown:
  path: markdown
  separator: ^\\n\\n\\n
  separator-notes: '^Note:'
  separator-vertical: ^\\n\\n
progress: true
sections: []
show_notes: false
theme: white
"""
                self.assertEqual(reader.read(), expected)


class RevealTestCase(TestCase):

    def check_xpaths(self, xhtml, csvfile):
        reader = csv.reader(csvfile)
        for (exp, val, attr) in reader:
            element = xhtml.find(exp, NSMAP)
            if val:
                if attr:
                    self.assertEqual(element.attrib[attr], val)
                else:
                    self.assertEqual(element.text, val)


class RevealPresentationCreatorCase(RevealTestCase):

    def setUp(self):
        name = self.__class__.__name__.replace('RevealPresentationCreatorCase',
                                               '').lower()

        self.config_path = os.path.join(DIR, name, 'config.yaml')
        self.xpath_expr_path = os.path.join(DIR, name, 'xpath.csv')

        self.tmpdir = tempfile.mkdtemp()

    def check_xpath_outputfile(self):
        os.chdir(self.tmpdir)
        creator = RevealPresentationCreator(config_path=self.config_path)
        creator.create()

        index = os.path.join(self.tmpdir, 'index.html')
        with open(index, 'r') as indexfile:
            xhtml = ET.parse(indexfile)
            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


class TitleRevealPresentationCreatorCase(RevealPresentationCreatorCase):

    def test_render_outputfile(self):
        """Render a title through the renderer"""
        self.check_xpath_outputfile()


class SummaryRevealPresentationCreatorCase(RevealPresentationCreatorCase):

    def test_render_outputfile(self):
        """Render a summary through the renderer"""
        self.check_xpath_outputfile()


class SectionsRevealPresentationCreatorCase(RevealPresentationCreatorCase):

    def test_render_outputfile(self):
        """Render a title through the renderer"""
        self.check_xpath_outputfile()


class MarkdownRevealPresentationCreatorCase(RevealPresentationCreatorCase):

    def test_render_outputfile(self):
        """Render a title through the renderer"""
        self.check_xpath_outputfile()


class EverythingRevealPresentationCreatorCase(RevealPresentationCreatorCase):

    def test_render_outputfile(self):
        """Render a title through the renderer"""
        self.check_xpath_outputfile()
