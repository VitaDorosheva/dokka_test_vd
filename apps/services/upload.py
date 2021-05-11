from datetime import datetime

from apps.services.tasks import generate_geo
from apps.db.models import db, Point, Upload
from apps.db.utils import bulk_insert


class UploadGeodataService():
    """saves uploaded data to database
    runs task to populate geo data"""
    def __init__(self, data):
        self.data = data
        self.upload_id = None
        self.links = []
        self.task_id = None
        self.status = ''

    def create_points(self):
        points = []
        for row in self.data:
            points.append({'name': row['Point'],
                           'latitude': row['Latitude'],
                           'longitude': row['Longitude'],
                           'upload_id': self.upload_id})

        """write to DB"""
        bulk_insert(db.session, Point, points)

    def populate_geo(self):
        task = generate_geo.delay(self.upload_id)
        self.task_id = task.id
        upload = Upload.query.filter_by(id=self.upload_id).first()
        upload.status = Upload.RUNNING
        upload.task_id = task.id
        db.session.commit()
        self.status = upload.status

    def process(self):
        upload = Upload(status='created', started=datetime.utcnow())
        db.session.add(upload)
        db.session.commit()
        self.upload_id = upload.id

        self.create_points()
        self.populate_geo()

        return self.task_id
