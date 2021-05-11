from datetime import datetime
from celery import Celery

from apps.db.models import db, Point, Link, Upload
from apps.db.utils import bulk_insert

from apps.services.geo import get_address, calculate_distance
from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task(name="generate_geo")
def generate_geo(upload_id):
    # populate address
    qs = Point.query.filter_by(upload_id=upload_id)
    for p in qs:
        p.address = get_address(p.latitude, p.longitude)
    db.session.commit()

    # generate links
    links = []
    points = list(qs)
    for i in range(len(points) - 1):
        for j in range(i+1, len(points)):
            p1 = points[i]
            p2 = points[j]
            name = p1.name + p2.name
            distance = calculate_distance((p1.latitude, p1.longitude), (p2.latitude, p2.longitude))
            links.append({'point_a_id': p1.id,
                          'point_b_id': p2.id,
                          'name': name,
                          'distance': distance
                          })
    bulk_insert(db.session, Link, links)

    upload = Upload.query.filter_by(id=upload_id).first()
    upload.status = Upload.DONE
    upload.finished = datetime.utcnow()

    db.session.commit()

    return True
