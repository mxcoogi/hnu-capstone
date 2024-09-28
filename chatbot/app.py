from flask import Flask , request
import sys
from chatbot import Chatbot
from common import model

hnu = Chatbot(model.basic)

app = Flask(__name__)

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
    response = hnu.send_request()
    hnu.add_response(response)
    response_message = hnu.get_response_content()
    return response_message