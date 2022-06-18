import json
from pathlib import Path
from unittest import result
from flights.models import Location, Country, Region, Settlement, Station
from flights.apps import SearchConfig


class FixtureBuilder:
	app_name = SearchConfig.name

	def __init__(self):
		self.json_fixture = list()

	def write_data(self):
		BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
		write_path = Path(BASE_DIR, *'fixture/search.json'.split('/'))
		with open(write_path, 'w') as file:
			file.write(json.dumps(self.json_fixture, indent=4))
			return write_path

	def __create_location(self, code, name):
		location = {
			'model': f'{self.app_name}.{Location.__name__}',
			'pk': code,
			'fields': {
				'name': name,
			}
		}
		return location

	def build_data(self, json_dump: dict) -> list[dict]:
		for country_i in json_dump['countries']:
			if country_i['codes'] and country_i['title']:
				location = self.__create_location(
					country_i['codes']['yandex_code'],
					country_i['title']
					)
			else:
				location = self.__create_location(
					'lNaN',
					'NaN'
				)
			country_dict = {
				'model': f'{self.app_name}.{Country.__name__}',
				'pk': location['pk'],
				'fields': {
					'location_ptr_id': location['pk'],
				}}
			region_result = self.__insert_region_data(country_i['regions'], country_dict)
			if region_result:
				self.json_fixture.append(location)
				self.json_fixture.append(country_dict)
				self.json_fixture+=region_result
		return self.json_fixture

	def __insert_region_data(self, array: list[dict], country: dict):
		result = list()
		location = None
		for region_i in array:
			if region_i['codes'] and region_i['title']:
				location = self.__create_location(
					region_i['codes']['yandex_code'],
					region_i['title']
				)
				region = {
					'model': f'{self.app_name}.{Region.__name__}',
					'pk': location['pk'],
					'fields': {
						'country_code': country['pk'],
						'location_ptr_id': location['pk'],
					}}
			else:
				region = {
					'model': f'{self.app_name}.{Region.__name__}',
					'pk': country['pk'],
					'fields': {
						'country_code': country['pk'],
						'location_ptr_id': country['fields']['location_ptr_id'],
					}}
			settelment_result = self.__insert_settlement_data(region_i['settlements'], region)
			if settelment_result:
				if location is not None:
					result.append(location)
				result.append(region)
				result+=settelment_result
		return result

	def __insert_settlement_data(self, array: list[dict], region: dict) -> list:
		result = list()
		location = None
		for settlement_i in array:
			if settlement_i['codes'] and settlement_i['title']:
				location = self.__create_location(
					settlement_i['codes']['yandex_code'],
					settlement_i['title']
				)
				settlement = {
					'model': f'{self.app_name}.{Settlement.__name__}',
					'pk': location['pk'],
					'fields': {
						'region_code': region['pk'],
						'location_ptr_id': location['pk'],
					}
				}
			else:
				settlement = {
					'model': f'{self.app_name}.{Settlement.__name__}',
					'pk': region['pk'],
					'fields': {
						'region_code': region['pk'],
						'location_ptr_id':  region['pk'],
					}
				}
			station_result = self.__insert_station_data(settlement_i['stations'], settlement)
			if station_result:
				if location is not None:
					result.append(location)
				result.append(settlement)
				result+=station_result
		return result

	def __insert_station_data(self, array: list[dict], settlement: dict) -> list:
		result = list()
		location = None
		for station_i in array:
			if station_i['codes'] and station_i['title'] and station_i['station_type'] == 'airport':
				location = self.__create_location(
					station_i['codes']['yandex_code'],
					station_i['title']
				)
				station = {
					'model': f'{self.app_name}.{Station.__name__}',
					'pk': location['pk'],
					'fields': {
						'settlement_code': settlement['pk'],
						'location_ptr_id': location['pk'],
						'station_type': station_i['station_type'],
					}
				}
				result.append(location)
				result.append(station)
		return result

