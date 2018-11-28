"""Test cases for zinnia.models_bases"""
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from events.models_bases import load_model_class
from events.models_bases.entry import AbstractEntry


class LoadModelClassTestCase(TestCase):

    def test_load_model_class(self):
        self.assertEqual(
            load_model_class('events.models_bases.entry.AbstractEntry'),
            AbstractEntry)
        self.assertRaises(ImproperlyConfigured,
                          load_model_class, 'invalid.path.models.Toto')
