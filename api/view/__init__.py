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

            user_id = payload['user_id']
            g.user_id = user_id
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
            user_id = credential['student_id']
            token = user_service.generate_access_token(user_id)

            return jsonify({
                'user_id' : user_id,
                'access_token' : token
            })
        else:
            return '', 401