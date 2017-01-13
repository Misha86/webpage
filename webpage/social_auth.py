from __future__ import unicode_literals
from decouple import config


# Модель пользователя. Здесь стандартная.
SOCIAL_AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.vk.VKOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

# Facebook #
# Для фейсбука, мы запрашиваем поля, и указываем локаль, вот таким вот образом.
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'ru_RU',
    'fields': 'id, name, email, picture',
    }

# А так мы запрашиваем дополнительные разрешения.
# Разрешения спрашиваются с первым запросом (authorize).
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = ['picture']


# VK #
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
# Чтобы запросить дополнительные поля, нужно указать их в EXTRA_DATA,
# специфика этого бекэнда.
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['photo_200_orig']


# ODNOKLASSNIKI #
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SCOPE = ['email']


# LINKEDIN #
# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry')]


# Проверка url перенаправления
SOCIAL_AUTH_SANITIZE_REDIRECTS = True


SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'message:list'
SOCIAL_AUTH_LOGIN_URL = 'message:enter'


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']


SOCIAL_AUTH_PROTECTED_USER_FIELDS = ["email", ]


# Python Social Auth
# Ключи

# Facebook #
SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET')

# VK #
SOCIAL_AUTH_VK_OAUTH2_KEY = config('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = config('SOCIAL_AUTH_VK_OAUTH2_SECRET')

# ODNOKLASSNIKI #
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = config('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY')
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = config('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET')
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = config('SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME')

# LINKEDIN #
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = config('SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = config('SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET')
