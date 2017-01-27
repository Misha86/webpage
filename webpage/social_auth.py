from __future__ import unicode_literals
from decouple import config


# Модель пользователя. Здесь стандартная.
SOCIAL_AUTH_USER_MODEL = 'auth.User'
import social.backends.odnoklassniki

import social.pipeline.social_auth
AUTHENTICATION_BACKENDS = (
    'social.backends.vk.VKOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    # 'webpage.pipeline.user_details'
)


# Facebook #
# Для фейсбука, мы запрашиваем поля, и указываем локаль, вот таким вот образом.
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'ru_RU',
    'fields': 'id, name, email, picture, link',
    }

# А так мы запрашиваем дополнительные разрешения.
# Разрешения спрашиваются с первым запросом (authorize).
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = ['picture', "link"]


# VK #
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
# Чтобы запросить дополнительные поля, нужно указать их в EXTRA_DATA,
# специфика этого бекэнда.
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['photo_50', 'city', 'domain']


# ODNOKLASSNIKI #
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_EXTRA_DATA = [('email', 'email'),
                                               ('pic_1', 'photo')]


# LINKEDIN #
# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'industry',   'public-profile-url',
                                               'picture-url', 'site-standard-profile-request',
                                               'api-standard-profile-request', 'location']

# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'),
                                          ('firstName', 'first_name'),
                                          ('lastName', 'last_name'),
                                          ('emailAddress', 'email_address'),
                                          ('headline', 'headline'),
                                          ('industry', 'industry'),

                                          ('pictureUrl', 'picture_url'),
                                          # ('pictureUrlsOriginal', 'picture-urls::(original)'),
                                          ('siteStandardProfileRequest', 'site_standard_profile_request'),
                                          ('publicProfileUrl', 'public_profile_url'),
                                          ('apiStandardProfileRequest', 'api_standard_profile_request'),
                                          ('location', 'location')]

# Проверка url перенаправления
SOCIAL_AUTH_SANITIZE_REDIRECTS = True


SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'message:list'
SOCIAL_AUTH_LOGIN_URL = 'message:enter'
SOCIAL_AUTH_LOGIN_ERROR_URL = 'message:enter'


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
