try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

import xml.etree.ElementTree as ET

from unittest import TestCase

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import os

import tempfile

import sys

import csv

import presentationhelper

from presentationhelper.reveal import (RevealPresentationCreator,
                                       RevealIndexRenderer)


NSMAP = {'xhtml': 'http://www.w3.org/1999/xhtml'}

DIR = os.path.dirname(os.path.realpath(__file__))
MODULE_DIR = os.path.dirname(presentationhelper.__file__)


class RevealTestCase(TestCase):

    def setUp(self):
        self.config_path = None
        self.xpath_expr_path = None

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

    def check_xpath_outputfile(self):
        with tempfile.NamedTemporaryFile() as stream:
            creator = RevealPresentationCreator(config_path=self.config_path,
                                                output_path=stream.name)
            creator.create()

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

            stream.close()

    @patch('sys.stdout', new_callable=StringIO)
    def check_xpath_stdout(self, mock_stdout):
        creator = RevealPresentationCreator(config_path=self.config_path)
        creator.create()

        mock_stdout.seek(0)
        xhtml = ET.parse(mock_stdout)

        with open(self.xpath_expr_path) as csvfile:
            self.check_xpaths(xhtml, csvfile)


class TitleRevealPresentationCreatorCase(RevealPresentationCreatorCase):

    def test_render_outputfile(self):
        """Render a title through the renderer (to an output file)"""
        self.check_xpath_outputfile()

    def test_render_stdout(self):
        """Render a title through the renderer (to stdout)"""
        self.check_xpath_stdout()


class RevealIndexRendererTestCase(RevealTestCase):

    def setUp(self):
        name = self.__class__.__name__.replace('RevealIndexRendererTestCase',
                                               '').lower()

        self.config_path = os.path.join(DIR, name, 'config.yaml')
        self.xpath_expr_path = os.path.join(DIR, name, 'xpath.csv')

    def check_xpath_stream(self):
        renderer = RevealIndexRenderer(config_path=self.config_path)

        with StringIO() as stream:
            renderer.output = stream
            renderer.render()

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    def check_xpath_outputfile(self):
        with tempfile.NamedTemporaryFile() as stream:
            renderer = RevealIndexRenderer(config_path=self.config_path,
                                           output_path=stream.name)
            renderer.render()

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    @patch('sys.stdout', new_callable=StringIO)
    def check_xpath_stdout(self, mock_stdout):
        renderer = RevealIndexRenderer(config_path=self.config_path)

        renderer.render()

        mock_stdout.seek(0)
        xhtml = ET.parse(mock_stdout)

        with open(self.xpath_expr_path) as csvfile:
            self.check_xpaths(xhtml, csvfile)

    def test_init_output_stdout(self):
        """Does a RevealIndexRenderer use stdout as its default output?"""
        renderer = RevealIndexRenderer()
        self.assertIs(renderer.output, sys.stdout)


class TitleRevealIndexRendererTestCase(RevealIndexRendererTestCase):

    def test_render_stream(self):
        """Render a title through the renderer (to a stream)"""
        self.check_xpath_stream()

    def test_render_file(self):
        """Render a title through the renderer (to an output file)"""
        self.check_xpath_outputfile()

    def test_render_stdout(self):
        """Render a title through the renderer (to stdout)"""
        self.check_xpath_stdout()


class SummaryRevealIndexRendererTestCase(RevealIndexRendererTestCase):
    def test_render_stream(self):
        """Render a summary through the renderer (to a stream)"""
        self.check_xpath_stream()

    def test_render_file(self):
        """Render a summary through the renderer (to an output file)"""
        self.check_xpath_outputfile()

    def test_render_stdout(self):
        """Render a summary through the renderer (to stdout)"""
        self.check_xpath_stdout()


class SectionsRevealIndexRendererTestCase(RevealIndexRendererTestCase):
    def test_render_stream(self):
        """Render sections through the renderer (to a stream)"""
        self.check_xpath_stream()

    def test_render_file(self):
        """Render sections through the renderer (to an output file)"""
        self.check_xpath_outputfile()

    def test_render_stdout(self):
        """Render sections through the renderer (to stdout)"""
        self.check_xpath_stdout()


class MarkdownRevealIndexRendererTestCase(RevealIndexRendererTestCase):
    def test_render_stream(self):
        """Render Markdown sections through the renderer (to a stream)"""
        self.check_xpath_stream()

    def test_render_file(self):
        """Render Markdown sections through the renderer (to an output file)"""
        self.check_xpath_outputfile()

    def test_render_stdout(self):
        """Render Markdown sections through the renderer (to stdout)"""
        self.check_xpath_stdout()


class EverythingRevealIndexRendererTestCase(RevealIndexRendererTestCase):
    def test_render_stream(self):
        """Render a full configuration through the renderer (to a stream)"""
        self.check_xpath_stream()

    def test_render_file(self):
        """Render a full configuration through the renderer (to an output
        file)"""
        self.check_xpath_outputfile()

    def test_render_stdout(self):
        """Render a full configuration through the renderer (to stdout)"""
        self.check_xpath_stdout()
