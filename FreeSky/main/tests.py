from django.test import TestCase
import unittest
from tests.test_views import AppViewsLoadsTestCaseMixin

# Create your tests here.
class MainViewTestCase(AppViewsLoadsTestCaseMixin, unittest.TestCase):

	expected_status_code = {
		'about-us/': 302,
	}

	def get_urls_patterns(self):
		from .urls import urlpatterns
		return urlpatterns
