HEREAPI_REVERSE_URL = 'https://revgeocode.search.hereapi.com/v1/revgeocode'
HEREAPI_API_KEY = 'WIKkKq5FT3r09tEDhM8lieCfktUSV6WjoSQ8KckQ254'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/d_test'
SQLALCHEMY_TRACK_MODIFICATIONS = False