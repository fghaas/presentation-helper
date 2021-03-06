# -*- coding: utf-8 -*-
import csv
import os
import shlex
import shutil
import tempfile
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET
import yaml

from unittest import TestCase

import presentationhelper
from presentationhelper.cli import main as climain, COMMAND as clicommand


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
        cliargs = ("%s -vv -F reveal create "
                   "-c %s") % (clicommand,
                               self.config_path)
        climain(shlex.split(cliargs))

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


class InvalidCLICallTestCase(TestCase):

    def test_invalid_config_file(self):
        cliargs = ("%s create "
                   "-c nonexistent.file") % clicommand

        # Using a non-existent config file should set the exit code to
        # ENOENT (2).
        with self.assertRaises(SystemExit) as se:
            climain(shlex.split(cliargs))
        self.assertEqual(se.exception.code, 2)


class DefaultConfigTestCase(TestCase):

    def test_default_config(self):
        """Does the default-config subcommand create a file with loadable
        YAML?"""
        with NamedTemporaryFile() as output:
            cliargs = ("%s -F reveal default-config "
                       "-o %s") % (clicommand, output.name)
            climain(shlex.split(cliargs))
            with open(output.name, 'r') as readback:
                d = yaml.safe_load(readback)
                self.assertIn('theme', d.keys())
