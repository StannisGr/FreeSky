from django.db import models
#  from django.contrib.postgres import fields


class Country(models.Model):
    code = models.CharField('Код', max_length=30, primary_key=True, null=False, blank=False)  # yandex_code notation
    name = models.CharField('Название', max_length=14, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Region(models.Model):
    code = models.CharField('Код', max_length=30, primary_key=True, null=False, blank=False)  # yandex_code notation
    country_code = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField('Название', max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Settlement(models.Model):
    code = models.CharField('Код', max_length=30, primary_key=True, null=False, blank=False)  # yandex_code notation
    region_code = models.ForeignKey(Region, on_delete=models.PROTECT)
    name = models.CharField('Название', max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Station(models.Model):
    code = models.CharField('Код', max_length=30, primary_key=True, null=False, blank=False)  # yandex_code notation
    name = models.CharField('Название', max_length=30, null=False, blank=False)
    settlement_code = models.ForeignKey(Settlement, on_delete=models.PROTECT, null=True, blank=True)
    station_type = models.CharField('Тип', max_length=30)

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'
