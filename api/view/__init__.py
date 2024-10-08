import jwt
from flask import request, jsonify, current_app, Response, g
from flask.json import JSONEncoder
from functools import wraps

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        
        return JSONEncoder.default(self, obj)
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                payload = None
            
            if payload is None: return Response(status=401)

            student_id = payload['student_id']
            g.student_id = student_id
        else:
            return Response(status=401)

        return f(*args, **kwargs)
    return decorated_function



def create_endpoints(app, services):
    app.json_encoder = CustomJSONEncoder
    user_service = services.user_service


    @app.route("/ping", methods = ['GET'])
    def ping():
        return "pong"
    @app.route("/sign-up", methods = ['POST'])
    def sign_up():
        new_user = request.json
        new_user= user_service.create_new_user(new_user)

        return jsonify(new_user)
    
    @app.route('/login', methods = ['POST'])
    def login():
        credential = request.json #학번 비번 들어옴
        authorized = user_service.login(credential)

        if authorized:
            student_id = credential['student_id']
            token = user_service.generate_access_token(student_id)

            return jsonify({
                'student_id' : student_id,
                'access_token' : token
            })
        else:
            return '', 401
        
        
    @app.route('/mypage', methods = ['GET'])
    @login_required
    def mypage():
        student_id = g.student_id
        user_info = user_service.user_info(student_id)
        return user_info
    
    
    @app.route('/mypage', methods = ['POST'])
    @login_required
    def edit_mypage():
        payload = request.json # 유저 페이지 수정 해야댐 여기서부터!!!
        user_info = user_service.user_info(g.student_id)
        for i in payload:
            user_info[i] = payload[i]
        edit_info = user_service.edit_user_info(user_info)
        return edit_info

    
    