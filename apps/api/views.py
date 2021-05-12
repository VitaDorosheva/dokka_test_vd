import codecs
import csv

from flask import request, make_response
from flask_jsonpify import jsonify

from apps.db.models import db, Upload, Point, Link
from apps.services.tasks import celery
from apps.services.upload import UploadGeodataService

from app import app, auth


@app.route('/api/calculateDistances', methods=['POST'])
@auth.login_required
def calculate_distances():
    file = request.files['file']
    if not file:
        return 'Upload a CSV file'
    data = []
    stream = codecs.iterdecode(file.stream, 'utf-8')
    for row in csv.DictReader(stream):
        if row:
            data.append(row)

    service = UploadGeodataService(data)
    id = service.process()
    output = {'task_id': id,
              'status': service.status}

    return make_response(jsonify(output), 200)


@app.route('/api/getResult/<result_id>', methods=['GET'])
@auth.login_required
def get_result(result_id):
    qs = Upload.query.filter_by(task_id=result_id)
    if qs.first() is None:
        message = f'Task {result_id} not found.'
        return make_response(jsonify({'message': message}), 404)

    upload = qs.first()
    status = upload.status

    if status != Upload.DONE:
        # obtain real status from task
        status = celery.AsyncResult(result_id).status
        data = []
    else:
        qs_points = Point.query.filter_by(upload_id=upload.id)
        p_ids = [p.id for p in qs_points]
        data = {'points': [{'name': p.name, 'address': p.address}
                           for p in qs_points],
                'links': [{'name': l.name, 'distance': l.distance}
                          for l in db.session.query(Link).filter((Link.point_a_id in p_ids) | (Link.point_b_id in p_ids))]}
    return make_response(jsonify({'task_id': result_id,
                                  'status': status,
                                  'data': data}), 200)


if __name__ == '__main__':
    app.run()
