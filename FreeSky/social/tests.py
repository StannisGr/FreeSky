from django.test import TestCase
import unittest
from tests.test_views import AppViewsLoadsTestCaseMixin


# Create your tests here.
class SocialViewTestCase(AppViewsLoadsTestCaseMixin, unittest.TestCase):

	url_prefix = '/social/'

	def get_urls_patterns(self):
		from .urls import urlpatterns
		return urlpatterns
