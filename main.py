# app.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db
from routes.feed import feed_bp
from routes.communities import communities_bp
from routes.events import events_bp
from routes.mentors import mentors_bp
from routes.auth import auth_bp
from routes.messages import messages_bp
from routes.upload import upload_bp
from routes.discover import discover_bp
import os

app = Flask(__name__)

# Upload klasörü
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max file size

# CORS
CORS(app)

# Database
db.init_app(app)

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(communities_bp)
app.register_blueprint(events_bp)
app.register_blueprint(mentors_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(discover_bp)

# Database tabloları oluştur
with app.app_context():
    db.create_all()
    print("[OK] Database tablolari olusturuldu!")

@app.route('/')
def index():
    return {'message': 'Campus Social API', 'status': 'running'}, 200

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # host='0.0.0.0' - Tüm network interfacelerinde dinle (mobil cihazlar için)
    app.run(debug=True, host='0.0.0.0', port=5000)