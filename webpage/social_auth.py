from __future__ import unicode_literals

# Модель пользователя. Здесь стандартная.
SOCIAL_AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.vk.VKOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)


# Для фейсбука, мы запрашиваем поля, и указываем локаль, вот таким вот образом.
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    # 'locale': 'ru_RU',
    'fields': 'id, name, email, picture',
    }

# А так мы запрашиваем дополнительные разрешения.
# Разрешения спрашиваются с первым запросом (authorize).
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Ключи
SOCIAL_AUTH_FACEBOOK_KEY = '702010003306076'
SOCIAL_AUTH_FACEBOOK_SECRET = '91b5f25150c536b9a5ab39187959517b'
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = ['picture']

# VK #
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
# Чтобы запросить дополнительные поля, нужно указать их в EXTRA_DATA,
# специфика этого бекэнда.
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['photo_200_orig']
# по умолчанию бекэнд будет использовать api версии 3.0
# SOCIAL_AUTH_VK_OAUTH2_API_VERSION = '5.5'


# Ключи
SOCIAL_AUTH_VK_OAUTH2_KEY = '5806264'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'JS3mCZ17ACGpRR7dZJ1Z'


# ODNOKLASSNIKI #
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SCOPE = ['email']
# Ключи
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = '1249422080'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = '2BD0DB4D3870B0144D39DF44'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = 'CBAMKJHLEBABABABA'

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
# Ключи
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '86xh8zkjixq1gl'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'udJ4GuXKW8NUpQ2Y'


# Проверка url перенаправления
SOCIAL_AUTH_SANITIZE_REDIRECTS = True


# SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'message:list'
# SOCIAL_AUTH_LOGIN_URL = 'message:enter'


SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']


SOCIAL_AUTH_PROTECTED_USER_FIELDS = ["email", ]