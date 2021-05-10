import codecs
import csv

from flask import request, make_response
from flask_jsonpify import jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
    return jsonify(id)
    return jsonify(data)


#     output ={
# 'task_id': 123,
# 'status': 'running'
# }
#
#     return make_response(jsonify(output), 200)


@app.route('/api/getResult/<result_id>', methods=['GET'])
@auth.login_required
def get_result(result_id):
    message = f'Task {result_id} not found.'
    return make_response(jsonify({"message": message}), 400)


if __name__ == '__main__':
     app.run(debug=True)

