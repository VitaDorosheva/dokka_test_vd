from celery import Celery

from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task(name="generate_geo")
def generate_geo(upload_id, data):


    return True