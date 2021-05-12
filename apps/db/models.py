from datetime import datetime

import sqlalchemy as sa

from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.declarative import declarative_base

from app import db

Base = declarative_base()


class Upload(db.Model):
    RUNNING = 'running'
    DONE = 'done'

    __tablename__ = 'upload'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String())
    task_id = db.Column(UUIDType, index=True)
    started = db.Column(sa.DateTime, default=datetime.utcnow)
    finished = db.Column(sa.DateTime)


class Point(db.Model):
    __tablename__ = 'point'

    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey("upload.id", ondelete="restrict"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    latitude = db.Column(sa.String(), nullable=False)
    longitude = db.Column(sa.String(), nullable=False)
    address = db.Column(sa.String())


class Link(db.Model):
    __tablename__ = 'link'

    id = db.Column(db.Integer, primary_key=True)
    point_a_id = db.Column(db.Integer, db.ForeignKey("point.id", ondelete="restrict"), nullable=False)
    point_b_id = db.Column(db.Integer, db.ForeignKey("point.id", ondelete="restrict"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    distance = db.Column(db.DECIMAL)
