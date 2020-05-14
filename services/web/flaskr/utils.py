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

# helpers for sanitizing post content


def check_newlines(content):
    msg_lines = content.count('\n')
    msg_length = len(content)

    # Find the ratio of newlines to characters
    line_ratio = msg_lines / msg_length

    # If a message is more than 3% newlines or has more than 100 newlines reject it
    if line_ratio > 0.2:
        return False
    elif msg_lines > 250:
        return False
    else:
        return True
