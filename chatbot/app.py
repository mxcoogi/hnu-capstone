from flask import Flask , request
from chatbot import Chatbot
from common import model
from function_calling import FunctionCalling, tools 
from characters import system_role, instruction
from common import model

app = Flask(__name__)

hnu = Chatbot(
    model = model.basic,
    system_role = system_role,
    instruction = instruction
    )
func_calling = FunctionCalling(model=model.basic)


        
@app.route("/chat-api", methods = ['POST'])
def chat_api():
    request_message = request.json['request_message']
    user_name = request.json['name']
    student_id = request.json['student_id']
    grade = request.json['grade']
    department = request.json['department']
    student_info = {
        'name' : user_name,
        'student_id' : student_id,
        'grade' : grade,
        'department' : department
    }
    hnu.add_user_message(request_message, student_info)
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