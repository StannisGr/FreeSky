from tests.test_settings import client


class AppViewsLoadsTestCaseMixin:

	expected_status_code: dict[str, int] = {}
	url_prefix: str = '/'

	def get_urls_patterns(self):
		raise NotImplementedError

	def test_base_urls_response(self):
		for url in self.get_urls_patterns():
			if not  url.pattern.regex.groups:
				route = url.pattern._route
				full_url = f'{self.url_prefix}{route}'
				response = client.get(full_url)
				self.assertEqual(response.status_code, self.expected_status_code.get(route, 200), f'[Error] Failed route: {full_url}')
