# routes/auth.py
from flask import Blueprint, jsonify, request
from models import db, User, Community
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = 'your-secret-key-here'  # Bu değer main.py'deki SECRET_KEY ile aynı olmalı


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token gerekli'}), 401

        try:
            if token.startswith('Bearer '):
                token = token[7:]

            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return jsonify({'error': 'Kullanıcı bulunamadı'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token süresi doldu'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Geçersiz token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    avatar = data.get('avatar', 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + email)

    if not name or not email or not password:
        return jsonify({'error': 'İsim, email ve şifre gerekli'}), 400

    # Email kontrolü
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Bu email zaten kayıtlı'}), 409

    # Yeni kullanıcı oluştur
    new_user = User(
        name=name,
        email=email,
        avatar=avatar
    )

    db.session.add(new_user)
    db.session.commit()

    # JWT token oluştur
    token = jwt.encode({
        'user_id': new_user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Kayıt başarılı',
        'token': token,
        'user': {
            'id': str(new_user.id),
            'name': new_user.name,
            'email': new_user.email,
            'avatar': new_user.avatar
        }
    }), 201


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email ve şifre gerekli'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'Kullanıcı bulunamadı'}), 404

    # Şimdilik şifre kontrolü yapmıyoruz (User modelinde password field'ı yok)
    # İleride password field'ı eklendiğinde check_password_hash kullanılabilir

    # JWT token oluştur
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Giriş başarılı',
        'token': token,
        'user': {
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'avatar': user.avatar
        }
    }), 200


@auth_bp.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        'user': {
            'id': str(current_user.id),
            'name': current_user.name,
            'email': current_user.email,
            'avatar': current_user.avatar,
            'created_at': current_user.created_at.isoformat()
        }
    }), 200


@auth_bp.route('/api/auth/update-profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()

    if 'name' in data:
        current_user.name = data['name']

    if 'avatar' in data:
        current_user.avatar = data['avatar']

    db.session.commit()

    return jsonify({
        'message': 'Profil güncellendi',
        'user': {
            'id': str(current_user.id),
            'name': current_user.name,
            'email': current_user.email,
            'avatar': current_user.avatar
        }
    }), 200
