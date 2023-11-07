from flask import Blueprint, request, current_app
from botapi.llm import context

chat = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat.route('/', methods=['GET'])
def get_home():
    args = request.args 
    question = args.get('q')
    current_app.logger.info(f"New chat request with prompt ${question}")

    if not question:
        return {"message": "No question provided"}, 400

    # get model from app context
    model = current_app.config['MODEL']
    response = model({"question": f"{context} {question}"})
    answer = response['answer']
    sources = response['sources']

    # return response
    return {"answer": answer, "sources": sources}, 200