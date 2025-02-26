from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['165.227.133.219', 'kadirdemirmatematik.com', 'www.kadirdemirmatematik.com']


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Database
# eğer db değiştirilirse aşağıdaki kodları kaldırıp yeni db yapısını ekleyin

# import dj_database_url

# DATABASES = {
#     'default': dj_database_url.parse(env('DATABASE_URL'))
# }
