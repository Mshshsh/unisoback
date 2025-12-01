# routes/discover.py
from flask import Blueprint, jsonify, request
from models import db, User
from sqlalchemy import func

discover_bp = Blueprint('discover', __name__)


@discover_bp.route('/api/discover/stats', methods=['GET'])
def get_discover_stats():
    """
    Discover ekranı için istatistikler
    """
    try:
        # Toplam kullanıcı sayısı
        total_users = User.query.count()

        # Bugün kayıt olan kullanıcılar (basitleştirilmiş)
        # Gerçek uygulamada created_at >= today filtresi kullanılmalı
        today_online = max(int(total_users * 0.35), 1)

        # Yeni eşleşmeler (basitleştirilmiş)
        new_matches = max(int(total_users * 0.07), 1)

        return jsonify({
            'stats': {
                'activeUsers': total_users,
                'onlineToday': today_online,
                'newMatches': new_matches
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
