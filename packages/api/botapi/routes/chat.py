from flask import Blueprint, request, current_app

chat = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat.route('/', methods=['GET'])
def get_home():
    args = request.args 
    question = args.get('q')

    if not question:
        return {"message": "No question provided"}, 400

    # get model from app context
    model = current_app.config['MODEL']
    response = model({"question": question})
    answer = response['answer']
    sources = response['sources']

    # return response
    return {"answer": answer, "sources": sources}, 200