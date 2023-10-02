"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from . import project_secrets


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kfb$#u9jo&gkpjai7i+l$y00gbu_-ro(sn)&3_@5f^fk4j!(ly'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INITIAL_APPS = [
    "modeltranslation",
    "jazzmin",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "werkzeug_debugger_runserver",
    "ckeditor",
    "phonenumber_field",
    "babel",
    "social_django",
    "rosetta",
    "debug_toolbar",
    "rest_framework",
    "django_filters",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "colorfield",
    "paypal.standard.ipn",
]

MY_APPS = [
    "core.apps.CoreConfig",
    "account.apps.AccountConfig",
    "product.apps.ProductConfig",
    "blog.apps.BlogConfig",
    "order.apps.OrderConfig",
]

INSTALLED_APPS = INITIAL_APPS + BASE_APPS + THIRD_PARTY_APPS + MY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "django.middleware.locale.LocaleMiddleware",  # Multilanguage
    "corsheaders.middleware.CorsMiddleware",  # CORS Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ========== MY MIDDLEWARE ==========
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug Toolbar
    "core.middleware.LoggingMiddleware",  # Custom Middleware Logging
    "core.middleware.BlacklistMiddleware",  # Custom Middleware Blacklist
    "core.middleware.AddUserIpsMiddleware",  # Custom Middleware AddUserIps
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # ========== MY CONTEXT PROCESSORS ==========
                "core.context_processors.shopping_cart_context",  # Custom Context Processors
                # Social Auth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# # PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'pavshop',
#         'USER': 'root',
#         'PASSWORD': 12345,
#         'HOST': 'localhost',
#         'PORT': 5432
#     }
# }


# Custom User model
AUTH_USER_MODEL = "account.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_TZ = True

USE_L10N = True

LANGUAGES = [
    ("en", "English"),
    ("az", "Azerbaijani"),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# Modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'az')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CKEditor configs
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        # 'height': 300,
        # 'width': '100%',
    },
}


# Jazzmin Settings
JAZZMIN_SETTINGS = {
    "site_title": "Pavshop Admin",
    "site_header": "Pavshop Admin",
    "site_brand": "Pavshop Admin Panel",
    "welcome_sign": "Welcome to Pavshop Admin panel",
    "language_chooser": True,
    # "changeform_format": "vertical_tabs",
    "copyright": "Pavshop",
    "topmenu_links": [
        {"name": _("VIEW SITE"), "url": "core:index_view", "new_window": True},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-history",

        # account APP
        "account.Country": "fas fa-globe",
        "account.City": "fas fa-city",
        "account.Address": "fas fa-map-marker-alt",
        "account.Position": "fas fa-briefcase",
        "account.User": "fas fa-user",
        "account.Blacklist": "fas fa-ban",

        # blog APP
        "blog.BlogCategory": "fas fa-folder",
        "blog.BlogTag": "fas fa-tag",
        "blog.Blog": "far fa-newspaper",
        "blog.BlogReview": "fas fa-comments",

        # core APP
        "core.Contact": "fas fa-envelope",
        "core.Newsletter": "fas fa-newspaper",
        "core.SubBanner": "fas fa-image",
        "core.ReklamBanner": "fas fa-bullhorn",

        # product APP
        "product.Color": "fas fa-palette",
        "product.Designer": "fas fa-pencil-ruler",
        "product.Brand": "fas fa-building",
        "product.Discount": "fas fa-percent",
        "product.ProductCategory": "fas fa-folder",
        "product.ProductTag": "fas fa-tag",
        "product.Product": "fas fa-cubes",
        "product.ProductVersion": "fas fa-cube",
        "product.ProductVersionImage": "fas fa-images",
        "product.ProductVersionReview": "fas fa-comments",
        "product.Wishlist": "fas fa-heart",
        "product.ShoppingCart": "fas fa-shopping-cart",
        "product.CartItem": "fas fa-shopping-basket",

        # order APP
        "order.BillingAddress": "fas fa-address-card",
        "order.ShippingAddress": "fas fa-shipping-fast",
        "order.Order": "fas fa-clipboard-list",
        "order.OrderItem": "fas fa-shopping-bag",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-navy",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}


# PasswordResetTokenGenerator token expiration time (6 hour)
PASSWORD_RESET_TIMEOUT = 6 * 60 * 60


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pavshop.project@gmail.com'
EMAIL_HOST_PASSWORD = 'vfvawfeqwoaaergj'
EMAIL_PORT = 587


# Social Login
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'
LOGIN_URL = 'login_view'
LOGIN_REDIRECT_URL = 'core:index_view'
LOGOUT_URL = 'logout_view'
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]
# LOGOUT_REDIRECT_URL = 'login_view'

# Github OAuth2 key and secret configuration
SOCIAL_AUTH_GITHUB_KEY = project_secrets.github_key
SOCIAL_AUTH_GITHUB_SECRET = project_secrets.github_secret

# Google OAuth2 key and secret configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = project_secrets.google_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = project_secrets.google_secret

# Facebook OAuth2 key and secret configuration
SOCIAL_AUTH_FACEBOOK_KEY = project_secrets.facebook_key             # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = project_secrets.facebook_secret       # App Secret

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'project_logs.log',
        },
    },
    'loggers': {
        'project_logs': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Debug Toolbar config
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}


# Rest Framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '5000/day',
    }
}


# Simple JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "TOKEN_OBTAIN_SERIALIZER": "account.api.serializers.CustomTokenObtainPairSerializer",
}


# Cookie Session(sessionid) expiration time
SESSION_COOKIE_AGE = timedelta(days=14).total_seconds()
# SESSION_COOKIE_NAME = "sessionid"


# CORS Headers config
CORS_ALLOW_ALL_ORIGINS: True


# Paypal config
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = "pavshop.project@business.example.com"
# PAYPAL_CURRENCY_CODE = "USD"


# Custom Variables config
CUSTOM_VARIABLES = {
    "MAX_PARENT_NESTING": 1,  # Specifies the maximum nesting level for parent comments
}
