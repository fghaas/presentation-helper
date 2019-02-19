# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

import xml.etree.ElementTree as ET

from unittest import TestCase

import os

import tempfile

import csv

import shutil

import presentationhelper

from presentationhelper.reveal import (RevealPresentationCreator)


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
