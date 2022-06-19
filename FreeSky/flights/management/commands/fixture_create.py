from django.core.management.base import BaseCommand
from django.conf import settings
from .services.utils import FixtureBuilder
from yaschedule.core import YaSchedule

class Command(BaseCommand):
	help = 'Creates fixture for db'

	def handle(self, *args, **options):
		path = self.__create_fixture()
		self.stdout.write(self.style.SUCCESS(f'INFO: Fixture created successfully and written to {path}'))

	def __create_fixture(self) -> str:
		yaschedule = YaSchedule(settings.YASHEDULE_API_TOKEN)
		response = yaschedule.get_all_stations()
		fixture_builder = FixtureBuilder()
		fixture_builder.build_data(json_dump=response)
		path = fixture_builder.write_data()
		return path
	