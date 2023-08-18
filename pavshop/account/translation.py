from modeltranslation.translator import translator, TranslationOptions
from .models import Country, City, Position


class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


class PositionTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Country, CountryTranslationOptions)
translator.register(City, CityTranslationOptions)
translator.register(Position, PositionTranslationOptions)
