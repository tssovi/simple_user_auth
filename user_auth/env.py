SECRET_KEY = '9l0as#*l7bp2&zt5q+gx6zxvh$^n_m!78i_md$oeq+7c*0k!qz'
DEBUG = True
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.CustomUser'

MAX_INVALID_LOG_IN_TRY = 3
ACCOUNT_LOCKED_FOR_MINUTES = 5