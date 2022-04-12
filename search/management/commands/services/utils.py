import json
from pathlib import Path
from search.models import Country, Region, Settlement, Station
from search.apps import SearchConfig


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

    def build_data(self, json_dump: dict) -> list[dict]:
        for country_i in json_dump['countries']:
            try:
                country_dict = {
                    'model': f'{self.app_name}.{Country.__name__}',
                    'pk': country_i['codes']['yandex_code'],
                    'fields': {
                        'name': country_i['title'],
                    }}
            except KeyError:
                country_dict = {
                    'model': f'{self.app_name}.{Country.__name__}',
                    'pk': 'lNaN',
                    'fields': {
                        'name': 'NaN',
                    }}
                print(f'EXCEPTION: KeyError\n DATA: {country_i}')
            self.json_fixture.append(country_dict)
            self.__insert_region_data(country_i['regions'], country_dict)
        return self.json_fixture

    def __insert_region_data(self, array: list[dict], country: dict):
        for region_i in array:
            if region_i['codes'] and region_i['title']:
                region = {
                    'model': f'{self.app_name}.{Region.__name__}',
                    'pk': region_i['codes']['yandex_code'],
                    'fields': {
                        'country_code': country['pk'],
                        'name': region_i['title']
                    }}
            else:
                region = {
                    'model': f'{self.app_name}.{Region.__name__}',
                    'pk': country['pk'],
                    'fields': {
                        'country_code': country['pk'],
                        'name': country['fields']['name'],
                    }}
            self.json_fixture.append(region)
            self.__insert_settlement_data(region_i['settlements'], region)

    def __insert_settlement_data(self, array: list[dict], region: dict):
        for settlement_i in array:
            if settlement_i['codes'] and settlement_i['title']:
                settlement = {
                    'model': f'{self.app_name}.{Settlement.__name__}',
                    'pk': settlement_i['codes']['yandex_code'],
                    'fields': {
                        'region_code': region['pk'],
                        'name': settlement_i['title']
                    }
				}
            else:
                settlement = {
                    'model': f'{self.app_name}.{Settlement.__name__}',
                    'pk': region['pk'],
                    'fields': {
                        'region_code': region['pk'],
                        'name': f'Региональный центр \"{region["fields"]["name"]}\"',
                    }
				}
            self.json_fixture.append(settlement)
            self.__insert_station_data(settlement_i['stations'], settlement)

    def __insert_station_data(self, array: list[dict], settlement: dict):
        for station_i in array:
            if station_i['codes'] and station_i['title'] and station_i['station_type'] == 'airport':
                station = {
                    'model': f'{self.app_name}.{Station.__name__}',
                    'pk': station_i['codes']['yandex_code'],
                    'fields': {
                        'settlement_code': settlement['pk'],
                        'name': station_i['title'],
                        'type': station_i['station_type'],
                    }
				}
                self.json_fixture.append(station)
            else:
                pass

