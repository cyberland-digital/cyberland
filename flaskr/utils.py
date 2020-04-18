import json
from flask import make_response, render_template


def send_json(data, status=200):
    if type(data) == list:
        json_string = json.dumps([dict(row) for row in data], default=str)
    else:
        json_string = json.dumps(dict(data), default=str)
    json_string = make_response(json_string)
    json_string.mimetype = "application/json"
    return json_string, status


def send_json_error(error, status=400):
    data = {'error': error}
    return send_json(data, status=status)


def send_text_template(file, status=200, context=None):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, status
