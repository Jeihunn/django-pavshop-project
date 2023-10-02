from modeltranslation.translator import translator, TranslationOptions
from .models import SubBanner, ReklamBanner


class SubBannerTranslationOptions(TranslationOptions):
    fields = ("title", "description", "breadcrumbs")


class ReklamBannerTranslationOptions(TranslationOptions):
    fields = ("title",)


translator.register(SubBanner, SubBannerTranslationOptions)
translator.register(ReklamBanner, ReklamBannerTranslationOptions)
