"""
Django settings for EJAT project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from pathlib import Path
from django.conf import global_settings
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ly76f6a_ngc%0w46^_d*tolyu%fl4(36+_$ly(mus-8gdi71(-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/



TIME_ZONE = 'Asia/Urumqi'

USE_I18N = True

USE_L10N = True

USE_TZ = True
LANGUAGE_CODE = 'en-us'

# 支持维吾尔语

gettext_noop = lambda s: s

LANGUAGES = (
    ('zh-hans', gettext_noop('Simplified Chinese')),
    ('zh-hant', gettext_noop('Traditional Chinese')),
    ('ug', gettext_noop('Uyghur')),
    ('en', gettext_noop('English')),
)


EXTRA_LANG_INFO = {
    'ug': {
        'bidi': False, # right-to-left
        'code': 'ug',
        'name': 'Uyghur',
        'name_local': u'\u0626\u06C7\u064A\u063A\u06C7\u0631 \u062A\u0649\u0644\u0649', #unicode codepoints here
    },
}

# Add custom languages not provided by Django
import django.conf.locale
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["ug"]

LOCALE_PATHS = ('D:\网上下载的软件\EJAT\EJAT\locale',)
# Application definition

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'register.apps.RegisterConfig',
    'login.apps.LoginConfig',
    'forget.apps.ForgotConfig',
    'public',
    'tinymce',
    'tinymce_upload',
    'django_celery_results',
    'reset.apps.ResetConfig',
    'index',  # apps.IndexConfig
    'category',
    'contact',
    'search',
    'about_us',
    "django_apscheduler",
]
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TASK_TIME_LIMIT = 120
CELERY_TIMEZONE = TIME_ZONE


# 使用 TinyPNG

TINYPNG_KEY = 'nTf7Zmwkbh2SBgND0vMFltDGnFJCwGhN'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]
# MIDDLEWARE=[
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
DEBUG_TOOLBAR_PATCH_SETTINGS = False
if DEBUG:
    # django debug toolbar
    INSTALLED_APPS.append('debug_toolbar')
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': 'https://code.jquery.com/jquery-1.11.2.min.js',
        # 或把jquery下载到本地然后取消下面这句的注释, 并把上面那句删除或注释掉
        # 'JQUERY_URL': '/static/js/jquery.js',
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }
INTERNAL_IPS = ("127.0.0.1",)



# DEBUG_TOOLBAR_CONFIG = {
#      # 引入jQuery库
#     'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
#     # 工具栏是否折叠
#     'SHOW_COLLAPSED': True,
#     # 是否显示工具栏
#     'SHOW_TOOLBAR_CALLBACK': lambda x: True,
# }




ROOT_URLCONF = 'EJAT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',#没有这一行会在模板里MEDIA_URL为空
            ],
        },
    },
]

WSGI_APPLICATION = 'EJAT.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'EJAT',
        'USER': 'root',
        'PASSWORD': '199954200061et',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_general_ci'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join('D:\\网上下载的软件\\EJAT\\', 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('D:\\网上下载的软件\\EJAT\\', 'media')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'register.MyUser'
AUTHENTICATION_BACKENDS = ['EJAT.my_libs.my_authenticate.My_authenticate']

EMAIL_HOST = "smtp.office365.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "ejatjonamar@outlook.com"
EMAIL_HOST_PASSWORD = "199954200061et"  # gakswtchefxpchae
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verification": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },
    "forgot_verification": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },
    "user_md5": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },
    "is_login": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },
    "index_page_cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/6",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },
    "celery_broker": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/7",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },
    "celery_backend": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/8",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True},
        }
    },

}
# 在用tinymce提交数据是报错
# RuntimeError: You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set. Django can't redirect to the slash URL while maintaining POST data. Change your form to point to 127.0.0.1:8000/contact/ (note the trailing slash), or set APPEND_SLASH=False in your Django settings.
# 意思是提交的路径必须以 / 结尾，或者设置APPEND_SLASH=False
APPEND_SLASH=False

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    # 'relative_urls': False,
    'width': 600,
    'height': 400,
    'language': 'ug',
    'plugins': "spellchecker,directionality,paste,searchreplace,image,media,code,codesample,imagetools",
    'toolbar': "spellchecker|directionality|paste|searchreplace|image|media|code|codesample|imagetools",
    'images_upload_url': "/upload/images/",
    'resize':'both',

    # 'images_upload_base_path':'media/tinymce/'
    # 'directionality': "{{ directionality }}",
    # 'spellchecker_languages' : "{{ spellchecker_languages }}",
    # 'spellchecker_rpc_url' : "{{ spellchecker_rpc_url }}"

}


