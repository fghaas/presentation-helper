# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

import presentationhelper

from presentationhelper.cli import CLI, COMMAND as clicommand

import xml.etree.ElementTree as ET

import csv

import os

import tempfile

import shlex

import shutil

NSMAP = {'xhtml': 'http://www.w3.org/1999/xhtml'}

DIR = os.path.dirname(os.path.realpath(__file__))
MODULE_DIR = os.path.dirname(presentationhelper.__file__)


class CLITestCase(TestCase):

    def setUp(self):
        name = self.__class__.__name__.replace('CLITestCase', '').lower()

        self.config_path = os.path.join(DIR, name, 'config.yaml')
        self.xpath_expr_path = os.path.join(DIR, name, 'xpath.csv')

        self.tmpdir = tempfile.mkdtemp()

    def check_xpaths(self, xhtml, csvfile):
        reader = csv.reader(csvfile)
        for (exp, val, attr) in reader:
            element = xhtml.find(exp, NSMAP)
            if val:
                if attr:
                    self.assertEqual(element.attrib[attr], val)
                else:
                    self.assertEqual(element.text, val)

    def check_xpath_cliargs_outputfile(self):
        os.chdir(self.tmpdir)
        cliargs = ("%s create -F reveal "
                   "-c %s") % (clicommand,
                               self.config_path)
        cli = CLI()
        cli.main(shlex.split(cliargs))

        index = os.path.join(self.tmpdir, 'index.html')
        with open(index, 'r') as indexfile:
            xhtml = ET.parse(indexfile)
            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


class TitleCLITestCase(CLITestCase):

    def test_cli_outputfile(self):
        """Render a title through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()


class SummaryCLITestCase(CLITestCase):

    def test_cli_outputfile(self):
        """Render a summary through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()


class SectionsCLITestCase(CLITestCase):

    def test_cli_outputfile(self):
        """Render sections through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()


class MarkdownCLITestCase(CLITestCase):

    def test_cli_outputfile(self):
        """Render Markdown sections through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()


class EverythingCLITestCase(CLITestCase):

    def test_cli_outputfile(self):
        """Render a full configuration through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()
