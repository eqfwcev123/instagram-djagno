"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import json
import os

import boto3

"""
AWS SECRETS
"""
# 환경변수
access_key = os.environ.get('AWS_SECRETS_MANAGER_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY')
region_name = 'ap-northeast-2'

session_kwargs = {
    'region_name': region_name
}

#### access_key 와 secret_key가 환경 변수에 존재할 경우
if access_key and secret_key:
    session_kwargs['aws_access_key_id'] = access_key
    session_kwargs['aws_secret_access_key'] = secret_key
else:
    session_kwargs['profile_name'] = 'wps-secrets-manager'
session = boto3.session.Session(**session_kwargs)

client = session.client(
    service_name='secretsmanager',  # AWS에 있는 SecretsManager사용
    region_name=region_name
)
secret_string = client.get_secret_value(SecretId='fastcp')['SecretString']
secret_data = json.loads(secret_string)  # 파이썬 딕셔너리로 변환
SECRETS = secret_data['instagram']

AWS_SECRETS_MANAGER_SECRETS_NAME = 'wps12'
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'instagram'
AWS_SECRETS_MANAGER_REGION_NAME = 'ap-northeast-2'
AWS_SECRETS_MANAGER_PROFILE = 'wps-secrets-manager'


"""
아마존 S3 사용
"""

# Boto3 와 S3 사용
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # 미디어/정적파일을 S3에 올리게 하기 설정
AWS_ACCESS_KEY_ID = SECRETS['AWS_ACCESS_KEY_ID']  # Boto3를 사용하기 위한 인증
AWS_SECRET_ACCESS_KEY = SECRETS['AWS_SECRET_ACCESS_KEY']  # Boto3를 사용하기 위한 인증
AWS_STORAGE_BUCKET_NAME = "wps-instagram-ldh2"  # 미디어/정적파일을 S3에 올리게 하기 설정
AWS_AUTO_CREATE_BUCKET = True  # True일 경우 AWS_STORAGE_BUCKET_NAME 에 지정되어 있는 bucket을 자동 생성한다
AWS_S3_REGION_NAME = "ap-northeast-2"

"""
경로 설정
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_URL = '/static/'
# os.path.dirname()은 한단계 위로 올라간다고 생각하면 된다.
ROOT_DIR = os.path.dirname(BASE_DIR)
# instagram/.media/
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# HTTPSCHEME + HOST + /Media/ + File주소

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9%65x8cg!9u2q)^#x++wg(d1usjjt!1imxbu_gj-e#e@&*!u7w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '15.164.228.223'
]
AUTH_USER_MODEL = 'members.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members.apps.MembersConfig',
    'posts.apps.PostsConfig',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'instagram',
        'USER': "ldh",
        'PASSWORD': SECRETS['POSTGRESQL_PASSWORD'],
        'HOST': 'wps12th-ldh.cninfzt6utzi.ap-northeast-2.rds.amazonaws.com',
        'PORT': 5432
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
