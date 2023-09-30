from modeltranslation.translator import translator, TranslationOptions
from .models import SubBanner


class SubBannerTranslationOptions(TranslationOptions):
    fields = ("title", "description", "breadcrumbs")


translator.register(SubBanner, SubBannerTranslationOptions)
