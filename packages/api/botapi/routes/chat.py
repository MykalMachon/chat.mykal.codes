from flask import Blueprint

chat = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat.route('/', methods=['POST'])
def get_home():
    return {"message": 'STUB: to be implemented'}