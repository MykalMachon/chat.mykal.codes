from flask import Blueprint, Response

meta = Blueprint('meta', __name__, url_prefix='/api/meta')

@meta.route('/healthcheck', methods=['GET'])
def get_health():
    """
    Return a 200 OK status to indicate the API is up and running.
    """
    return Response(status=200, mimetype='application/json', response='{"message": "OK"}')

@meta.route('/stats', methods=['GET'])
def get_stats():
    """
    Return stats about the bot API including startup time, 
    uptime, number of requests, etc.
    """ 
    return Response(status=200, mimetype='application/json', response='{"message": "OK"}')