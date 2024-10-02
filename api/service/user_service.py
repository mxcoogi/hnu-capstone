import bcrypt
import jwt
from datetime import datetime, timedelta
##user서비스 구현해야댐 
class UserService:
    def __init__(self, user_dao, config):
        self.user_dao = user_dao
        self.config = config
    
    def create_new_user(self, new_user):
        new_user['password'] = bcrypt.hashpw(
            new_user['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )
        new_user_id = self.user_dao.insert_user(new_user)

        return new_user_id
    
    def login(self, credential):
        student_id = credential['student_id']
        password = credential['password']
        user_credential = self.user_dao.get_user_id_and_password(student_id)

        authorized = user_credential and bcrypt.checkpw(password.encode('UTF-8'),
                                                        user_credential['hashed_password'].encode('UTF-8'))

        return authorized
    
    def generate_access_token(self, student_id):
        payload = self.user_info(student_id)
        payload['exp'] = datetime.utcnow() + timedelta(seconds= 60 * 60 * 24)
        token = jwt.encode(payload, self.config['JWT_SECRET_KEY'], 'HS256')

        return token
    
    def user_info(self, student_id):

        user_info = self.user_dao.get_user_info(student_id)
        return user_info
    
    def edit_user_info(self, payload):
        res = self.user_dao.edit_user_info(payload)
        return res
