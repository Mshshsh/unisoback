# routes/mentors.py
from flask import Blueprint, jsonify, request
from models import db, Mentor, User, MentorExpertise

mentors_bp = Blueprint('mentors', __name__)

@mentors_bp.route('/api/mentors', methods=['GET'])
def get_mentors():
    user_id = request.args.get('user_id', type=int)
    filter_type = request.args.get('filter', 'all')  # 'all', 'available', 'following'
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    user = User.query.get_or_404(user_id)
    
    # Base query
    query = Mentor.query
    
    # Filter by availability
    if filter_type == 'available':
        query = query.filter(Mentor.availability == 'available')
    
    # Filter by following
    elif filter_type == 'following':
        query = query.filter(Mentor.followers.any(id=user_id))
    
    # Pagination
    mentors = query.order_by(Mentor.rating.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )
    
    result = []
    for mentor in mentors.items:
        # Kullanıcının bu mentoru takip edip etmediğini kontrol et
        is_following = user in mentor.followers
        
        # Expertise
        expertise = [exp.skill for exp in mentor.expertise]
        
        mentor_data = {
            'id': str(mentor.id),
            'name': mentor.user.name,
            'avatar': mentor.user.avatar,
            'title': mentor.title,
            'company': mentor.company,
            'expertise': expertise,
            'availability': mentor.availability,
            'rating': mentor.rating,
            'sessionsCompleted': mentor.sessions_completed,
            'bio': mentor.bio,
            'responseTime': mentor.response_time,
            'isFollowing': is_following
        }
        
        result.append(mentor_data)
    
    return jsonify({
        'mentors': result,
        'page': page,
        'total_pages': mentors.pages,
        'total_items': mentors.total
    }), 200


@mentors_bp.route('/api/mentors/<int:mentor_id>/follow', methods=['POST'])
def toggle_follow(mentor_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    mentor = Mentor.query.get_or_404(mentor_id)
    user = User.query.get_or_404(user_id)
    
    # Kullanıcı zaten takip ediyor mu?
    is_following = user in mentor.followers
    
    if is_following:
        # Takibi kaldır
        mentor.followers.remove(user)
        db.session.commit()
        is_following = False
    else:
        # Takip et
        mentor.followers.append(user)
        db.session.commit()
        is_following = True
    
    return jsonify({
        'isFollowing': is_following
    }), 200