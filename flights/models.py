from django.db import models

# from django.contrib.postgres import fields
class Location(models.Model):
	code = models.CharField('Код', max_length=30, primary_key=True, null=False, blank=False)
	name = models.CharField('Название', max_length=14, null=False, blank=False)

	class Meta:
		verbose_name = 'Локация'
		verbose_name_plural = 'Локации'
		ordering = ['name']
	
	def __str__(self) -> str:
		return f'{self.name}'
	
	def __repr__(self) -> str:
		return {'class': self.__class__, **self.__dict__}

class Country(Location):
	
	class Meta:
		verbose_name = 'Страна'
		verbose_name_plural = 'Страны'

class Region(Location):
	country_code = models.ForeignKey(Country, on_delete=models.PROTECT)

	class Meta:
		verbose_name = 'Регион'
		verbose_name_plural = 'Регионы'

class Settlement(Location):
    region_code = models.ForeignKey(Region, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Station(Location):
    settlement_code = models.ForeignKey(Settlement, on_delete=models.PROTECT, null=True, blank=True)
    station_type = models.CharField('Тип', max_length=30)

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'
