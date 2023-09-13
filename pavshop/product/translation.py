from modeltranslation.translator import translator, TranslationOptions
from .models import ProductCategory, Product, ProductVersion


class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


class ProductVersionTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


translator.register(ProductCategory, ProductCategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(ProductVersion, ProductVersionTranslationOptions)
