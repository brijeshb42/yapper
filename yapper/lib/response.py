from flask import jsonify


def json_error(code=400, data=''):
    return jsonify(type='error', data=data), code


def json_success(data=''):
    return jsonify(type='success', data=data)
