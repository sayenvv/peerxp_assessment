from .local import *

'''
  when you want to switch sqlite to postgres you follow these steps

  1) change in manage.py
    
    - change from local to dev to access this page
'''

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'acme',

        'USER': 'acme_user',

        'PASSWORD': 'acme123',

        'HOST': 'localhost',

        'PORT': '5432',

    }

}
