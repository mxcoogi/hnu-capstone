from common import client, model
from pprint import pprint

class Chatbot:

    def __init__(self, model):
        self.context = [{"role": "system", "content": "한남대학교 학사관리챗봇."}]
        self.model = model

    def add_user_message(self, message, student_info):
        self.context.append({"role": "user", "content": message})
        self.student_info = {
            'name' : student_info['name'],
            'student_id' : student_info['student_id'],
            'grade' : student_info['grade']
        }
        self.context.append({"role" : "system" , "content" : f"name : {student_info['name']}, student_id : {student_info['student_id']}, grade : {student_info['grade']}, department : {student_info['department']}" })

    def send_request(self):
        try:
            response = client.chat.completions.create(
                model=self.model, 
                messages=self.context
            ).model_dump()
            return response
        except Exception as e:
            print(f"요청 중 오류 발생: {e}")
            return None

    def add_response(self, response):
        self.context.append({
                "role" : response['choices'][0]['message']["role"],
                "content" : response['choices'][0]['message']["content"],
            }
        )

    def get_response_content(self):
        return self.context[-1]['content']

