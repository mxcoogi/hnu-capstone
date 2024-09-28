from common import client, makeup_response
import math

class Chatbot:

    def __init__(self, model, system_role, instruction):
        self.context = [{"role": "system", "content": system_role}]
        self.model = model
        self.instruction = instruction
        self.max_token_size = 16 * 1024
        self.available_token_rate = 0.9

    def add_user_message(self, message, student_info):
        self.context.append({"role": "user", "content": message})
        self.student_info = {
            'name' : student_info['name'],
            'student_id' : student_info['student_id'],
            'grade' : student_info['grade']
        }
        self.context.append({"role" : "system" , "content" : f"name : {student_info['name']}, student_id : {student_info['student_id']}, grade : {student_info['grade']}, department : {student_info['department']}" })

    def _send_request(self):
        try:
            response = client.chat.completions.create(
                model=self.model, 
                messages=self.context,
                temperature=0,
                top_p=1,
                max_tokens=256,
                frequency_penalty=0,
                presence_penalty=0
            ).model_dump()
            return response
        except Exception as e:
            print(f"요청 중 오류 발생: {e}")
            return None
    
    def send_request(self):
        self.context[-1]['content'] += self.instruction
        return self._send_request()

    def add_response(self, response):
        self.context.append({
                "role" : response['choices'][0]['message']["role"],
                "content" : response['choices'][0]['message']["content"],
            }
        )

    def get_response_content(self):
        return self.context[-1]['content']

    def clean_context(self):
        for idx in reversed(range(len(self.context))):
            if self.context[idx]["role"] == "user":
                self.context[idx]["content"] = self.context[idx]["content"].split("instruction:\n")[0].strip()
                break

    def handle_token_limit(self, response):
        # 누적 토큰 수가 임계점을 넘지 않도록 제어한다.
        try:
            current_usage_rate = response['usage']['total_tokens'] / self.max_token_size
            exceeded_token_rate = current_usage_rate - self.available_token_rate
            if exceeded_token_rate > 0:
                remove_size = math.ceil(len(self.context) / 10)
                self.context = [self.context[0]] + self.context[remove_size+1:]
        except Exception as e:
            print(f"handle_token_limit exception:{e}")