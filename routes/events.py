# routes/events.py
from flask import Blueprint, jsonify, request
from models import db, Event, User, Community
from sqlalchemy import or_

events_bp = Blueprint('events', __name__)

@events_bp.route('/api/events', methods=['GET'])
def get_events():
    user_id = request.args.get('user_id', type=int)
    filter_type = request.args.get('filter', 'all')  # 'all' or 'interested'
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    user = User.query.get_or_404(user_id)
    
    # Base query
    query = Event.query
    
    # Filter by interested
    if filter_type == 'interested':
        query = query.filter(Event.interested_users.any(id=user_id))
    
    # Search filter
    if search:
        query = query.join(Community).filter(
            or_(
                Event.title.ilike(f'%{search}%'),
                Community.name.ilike(f'%{search}%')
            )
        )
    
    # Pagination
    events = query.order_by(Event.date.asc()).paginate(
        page=page, per_page=limit, error_out=False
    )
    
    result = []
    for event in events.items:
        # Kullanıcının bu etkinliğe ilgi gösterip göstermediğini kontrol et
        is_interested = user in event.interested_users
        
        event_data = {
            'id': str(event.id),
            'title': event.title,
            'community': event.community.name,
            'communityAvatar': event.community.avatar,
            'date': event.date.isoformat(),
            'time': event.time,
            'location': event.location,
            'image': event.image,
            'interested': len(event.interested_users),
            'isInterested': is_interested,
            'description': event.description,
            'capacity': event.capacity
        }
        
        result.append(event_data)
    
    return jsonify({
        'events': result,
        'page': page,
        'total_pages': events.pages,
        'total_items': events.total
    }), 200


@events_bp.route('/api/events/<int:event_id>/interest', methods=['POST'])
def toggle_interest(event_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    event = Event.query.get_or_404(event_id)
    user = User.query.get_or_404(user_id)
    
    # Kullanıcı zaten ilgileniyor mu?
    is_interested = user in event.interested_users
    
    if is_interested:
        # İlgiyi kaldır
        event.interested_users.remove(user)
        db.session.commit()
        is_interested = False
    else:
        # İlgi göster
        event.interested_users.append(user)
        db.session.commit()
        is_interested = True
    
    interested_count = len(event.interested_users)
    
    return jsonify({
        'isInterested': is_interested,
        'interested': interested_count
    }), 200