from flask import jsonify

def generate_response(data=None, message=None, status=200):
    response = {}
    if data is not None:
        response['data'] = data
    if message is not None:
        response['message'] = message
    return jsonify(response), status

def handle_error(e):
    return jsonify({'message': str(e)}), 400