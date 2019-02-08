from unittest import TestCase

from presentationhelper.cli import CLI

import xml.etree.ElementTree as ET

from io import StringIO

import csv

import os

import sys

import tempfile

NSMAP = {'xhtml': 'http://www.w3.org/1999/xhtml'}

DIR = os.path.dirname(os.path.realpath(__file__))


class IndexTestCase(TestCase):

    def setUp(self):
        name = self.__class__.__name__.replace('IndexTestCase', '').lower()

        self.config_path = os.path.join(DIR, name, 'config.yaml')
        self.xpath_expr_path = os.path.join(DIR, name, 'xpath.csv')

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
        cli.setup_config(self.config_path)

        with StringIO() as stream:
            cli.render(stream)

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)

    def check_xpath_cliargs_stream(self):
        cliargs = [
            '-c', self.config_path
        ]
        cli = CLI()
        with StringIO() as stream:
            try:
                sys.stdout = stream
                cli.main(cliargs)

                stream.seek(0)
                xhtml = ET.parse(stream)

                with open(self.xpath_expr_path) as csvfile:
                    self.check_xpaths(xhtml, csvfile)
            finally:
                sys.stdout = sys.__stdout__

    def check_xpath_cliargs_file(self):
        with tempfile.NamedTemporaryFile() as stream:
            cliargs = [
                '-c', self.config_path,
                '-o', stream.name
            ]
            cli = CLI()
            cli.main(cliargs)

            stream.seek(0)
            xhtml = ET.parse(stream)

            with open(self.xpath_expr_path) as csvfile:
                self.check_xpaths(xhtml, csvfile)


class TitleIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        self.check_xpath()

    def test_cli_stream(self):
        self.check_xpath_cliargs_stream()

    def test_cli_file(self):
        self.check_xpath_cliargs_file()


class SummaryIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        self.check_xpath()

    def test_cli_stream(self):
        self.check_xpath_cliargs_stream()

    def test_cli_file(self):
        self.check_xpath_cliargs_file()


class SectionsIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        self.check_xpath()

    def test_cli_stream(self):
        self.check_xpath_cliargs_stream()

    def test_cli_file(self):
        self.check_xpath_cliargs_file()


class MarkdownIndexTestCase(IndexTestCase):

    def test_index_renderer(self):
        self.check_xpath()

    def test_cli_stream(self):
        self.check_xpath_cliargs_stream()

    def test_cli_file(self):
        self.check_xpath_cliargs_file()


class EverythingIndexTestCase(IndexTestCase):

    def test_index(self):
        self.check_xpath()

    def test_cli_stream(self):
        self.check_xpath_cliargs_stream()

    def test_cli_file(self):
        self.check_xpath_cliargs_file()
