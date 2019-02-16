from unittest import TestCase

import presentationhelper

from presentationhelper.cli import CLI, main as climain, COMMAND as clicommand

import xml.etree.ElementTree as ET

from io import StringIO

import csv

import os

import sys

import tempfile

import shlex

NSMAP = {'xhtml': 'http://www.w3.org/1999/xhtml'}

DIR = os.path.dirname(os.path.realpath(__file__))
MODULE_DIR = os.path.dirname(presentationhelper.__file__)


class IndexTestCase(TestCase):

    def setUp(self):
        name = self.__class__.__name__.replace('IndexTestCase', '').lower()

        self.config_path = os.path.join(DIR, name, 'config.yaml')
        self.xpath_expr_path = os.path.join(DIR, name, 'xpath.csv')
        self.template_path = os.path.join(MODULE_DIR,
                                          'templates',
                                          'reveal',
                                          'index.html.j2')

    def check_xpaths(self, xhtml, csvfile):
        reader = csv.reader(csvfile)
        for (exp, val, attr) in reader:
            element = xhtml.find(exp, NSMAP)
            if val:
                if attr:
                    self.assertEqual(element.attrib[attr], val)
                else:
                    self.assertEqual(element.text, val)

    def check_xpath(self):
        cli = CLI()
        cli.flavor = 'reveal'
        cli.setup_config(self.config_path)

        with StringIO() as stream:
            cli.render(stream)

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    def check_xpath_cliargs_stream(self):
        cliargs = "%s reveal -c %s" % (clicommand, self.config_path)
        cli = CLI()
        with StringIO() as stream:
            try:
                sys.stdout = stream
                cli.main(shlex.split(cliargs))

                stream.seek(0)
                xhtml = ET.parse(stream)

                with open(self.xpath_expr_path) as csvfile:
                    self.check_xpaths(xhtml, csvfile)
            finally:
                sys.stdout = sys.__stdout__

    def check_xpath_cliargs_outputfile(self):
        with tempfile.NamedTemporaryFile() as stream:
            cliargs = "%s reveal -c %s -o %s" % (clicommand,
                                                 self.config_path,
                                                 stream.name)
            cli = CLI()
            cli.main(shlex.split(cliargs))

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    def check_xpath_cliargs_templatefile_outputfile(self):
        with tempfile.NamedTemporaryFile() as stream:
            for flavor in ['reveal', 'generic']:
                cliargs = ("%s reveal -c %s "
                           "-t %s -o %s") % (clicommand,
                                             self.config_path,
                                             self.template_path,
                                             stream.name)
                climain(shlex.split(cliargs))

                stream.seek(0)
                xhtml = ET.parse(stream)

                with open(self.xpath_expr_path) as csvfile:
                    self.check_xpaths(xhtml, csvfile)


class TitleIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        """Render a title through the renderer"""
        self.check_xpath()

    def test_cli_stream(self):
        """Render a title through the CLI (to stdout)"""
        self.check_xpath_cliargs_stream()

    def test_cli_outputfile(self):
        """Render a title through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()

    def test_cli_templatefile_outputfile(self):
        """
        Render a title through the CLI (to a file, with a custom
        template)
        """
        self.check_xpath_cliargs_templatefile_outputfile()


class SummaryIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        """Render a summary through the renderer"""
        self.check_xpath()

    def test_cli_stream(self):
        """Render a summary through the CLI (to stdout)"""
        self.check_xpath_cliargs_stream()

    def test_cli_outputfile(self):
        """Render a summary through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()

    def test_cli_templatefile_outputfile(self):
        """
        Render a summary through the CLI (to a file, with a custom
        template)
        """
        self.check_xpath_cliargs_templatefile_outputfile()


class SectionsIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        """Render sections through the renderer"""
        self.check_xpath()

    def test_cli_stream(self):
        """Render sections through the CLI (to stdout)"""
        self.check_xpath_cliargs_stream()

    def test_cli_outputfile(self):
        """Render sections through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()

    def test_cli_templatefile_outputfile(self):
        """
        Render sections through the CLI (to a file, with a custom
        template)
        """
        self.check_xpath_cliargs_templatefile_outputfile()


class MarkdownIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        """Render Markdown sections through the renderer"""
        self.check_xpath()

    def test_cli_stream(self):
        """Render Markdown sections through the CLI (to stdout)"""
        self.check_xpath_cliargs_stream()

    def test_cli_outputfile(self):
        """Render Markdown sections through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()

    def test_cli_templatefile_outputfile(self):
        """
        Render Markdown sections through the CLI (to a file, with a
        custom template)
        """
        self.check_xpath_cliargs_templatefile_outputfile()


class EverythingIndexTestCase(IndexTestCase):

    def test_index(self):
        """Render a full configuration through the renderer"""
        self.check_xpath()

    def test_cli_stream(self):
        """Render a full configuration through the CLI (to stdout)"""
        self.check_xpath_cliargs_stream()

    def test_cli_outputfile(self):
        """Render a full configuration through the CLI (to a file)"""
        self.check_xpath_cliargs_outputfile()

    def test_cli_templatefile_outputfile(self):
        """
        Render a full configuration through the CLI (to a file, with a
        custom template)
        """
        self.check_xpath_cliargs_templatefile_outputfile()
