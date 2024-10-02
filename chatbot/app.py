from flask import Flask , request
from chatbot import Chatbot
from common import model
from function_calling import FunctionCalling, tools 
from characters import system_role, instruction
from common import model
import jwt
import config

app = Flask(__name__)

hnu = Chatbot(
    model = model.basic,
    system_role = system_role,
    instruction = instruction
    )
func_calling = FunctionCalling(model=model.basic)


        
@app.route("/chat-api", methods = ['POST'])
def chat_api():
    access_token = request.headers.get('Authorization')
    if access_token is None:
        return '토큰이 필요합니다', 401
    
    try:
        payload = jwt.decode(access_token, config.JWT_SECRET_KEY, 'HS256')
    except jwt.InvalidTokenError:
        return '사용자 확인 안댐', 401

    request_message = request.json['request_message']
    hnu.add_user_message(request_message, payload)
    analyzed, analyzed_dict = func_calling.analyze(request_message, tools)
    if analyzed_dict.get("tool_calls"):
        response = func_calling.run(analyzed, analyzed_dict, hnu.context[:])
        hnu.add_response(response)
    else:
        response = hnu.send_request()
        hnu.add_response(response)

    response_message = hnu.get_response_content()
    hnu.handle_token_limit(response)
    hnu.clean_context()
    return response_message