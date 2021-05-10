from uuid import uuid4

from apps.services.tasks import generate_geo
from apps.db.models import Points
from apps.db.utils import bulk_insert
from app import db


class UploadGeodataService():
    """saves uploaded data to database
    runs task to populate geo data"""
    def __init__(self, data):
        self.data = data
        self.upload_uuid = uuid4()
        self.links = []
        self.task_id = None

    def create_points(self):
        points = []
        for row in self.data:
            points.append({'name': row['Point'],
                           'latitude': row['Latitude'],
                           'longitude': row['Longotude'],
                           'upload_id': self.upload_uuid})

        """write to DB"""
        bulk_insert(db.session, Points, points)

    def populate_geo(self):
        task = generate_geo.delay(self.upload_uuid, self.data)
        self.task_id = task.id

    def process(self):
        # upload = Uploads(id=self.upload_uuid,
        #                  status=,
        #                  task_id=)
        self.create_points()
        self.populate_geo()

        return self.upload_uuid
