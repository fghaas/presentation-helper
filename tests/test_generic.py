# -*- coding: utf-8 -*-
from unittest import TestCase

from tempfile import TemporaryDirectory
import os
import shutil

from presentationhelper.generic import (PresentationCreator,
                                        TemplateRendererException)

DIR = os.path.dirname(os.path.realpath(__file__))


class PresentationCreatorTestCase(TestCase):

    def setUp(self):
        name = self.__class__.__name__.replace('PresentationCreatorTestCase',
                                               '').lower()

        self.config_path = os.path.join(DIR, name, 'config.yaml')
        self.tmpdir = TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()


class TitlePresentationCreatorTestCase(PresentationCreatorTestCase):

    def test_no_templates(self):
        # The generic presentation creator does not contain any
        # templates by the default, and neither does the loaded
        # config; this should fail.
        with self.assertRaises(TemplateRendererException):
            c = PresentationCreator(config_path=self.config_path)  # noqa: F841


class TemplateDirPresentationCreatorTestCase(PresentationCreatorTestCase):

    def test_custom_template_dir(self):
        os.chdir(self.tmpdir.name)
        c = PresentationCreator(config_path=self.config_path)
        c.create()

        foo = os.path.join(self.tmpdir.name, 'foo')
        with open(foo, 'r') as foofile:
            self.assertIn(foofile.read(), "Superfrobnicate me")


class LocalTemplatePresentationCreatorTestCase(PresentationCreatorTestCase):

    def test_custom_template_file(self):
        dest = self.tmpdir.name

        for f in [self.config_path,
                  os.path.join(os.path.dirname(self.config_path),
                               'bar.j2')]:
            shutil.copy(f, dest)

        os.chdir(dest)
        c = PresentationCreator(config_path='config.yaml')
        c.create()

        bar = os.path.join(self.tmpdir.name, 'bar')
        with open(bar, 'r') as barfile:
            self.assertIn(barfile.read(), "Superfrobnicate me")
