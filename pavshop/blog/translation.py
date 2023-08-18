from modeltranslation.translator import translator, TranslationOptions
from .models import BlogCategory, Blog


class BlogCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(BlogCategory, BlogCategoryTranslationOptions)
translator.register(Blog, BlogTranslationOptions)
