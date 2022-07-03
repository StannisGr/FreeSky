import unittest
from django.test import TestCase
from tests.test_views import AppViewsLoadsTestCaseMixin
from user.models import User


# Create your tests here.
class UserViewTestCase(AppViewsLoadsTestCaseMixin, unittest.TestCase):

	expected_status_code = {
		'profile/': 302,
	}

	url_prefix = '/user/'

	def get_urls_patterns(self):
		from .urls import urlpatterns
		return urlpatterns