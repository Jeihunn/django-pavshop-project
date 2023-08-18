from modeltranslation.translator import translator, TranslationOptions
from .models import ProductCategory, Color, Product, ProductVersion


class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class ColorTranslationOptions(TranslationOptions):
    fields = ('name',)


class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


class ProductVersionTranslationOptions(TranslationOptions):
    fields = ('description',)


translator.register(ProductCategory, ProductCategoryTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(ProductVersion, ProductVersionTranslationOptions)
