# routes/communities.py
from flask import Blueprint, jsonify, request
from models import db, Community, User, CommunityTag, Post, Event
from sqlalchemy import or_

communities_bp = Blueprint('communities', __name__)

@communities_bp.route('/api/communities', methods=['GET'])
def get_communities():
    user_id = request.args.get('user_id', type=int)
    category = request.args.get('category')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    # Base query
    query = Community.query
    
    # Category filter
    if category and category != 'Tümü':
        query = query.filter(Community.category == category)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                Community.name.ilike(f'%{search}%'),
                Community.description.ilike(f'%{search}%')
            )
        )
    
    # Pagination
    communities = query.order_by(Community.created_at.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )
    
    result = []
    for community in communities.items:
        # Kullanıcının bu topluluğu takip edip etmediğini kontrol et
        is_following = user_id in [follower.id for follower in community.followers]
        
        # Tags
        tags = [tag.tag for tag in community.tags]
        
        # Upcoming events (next 30 days)
        upcoming_events = Event.query.filter(
            Event.community_id == community.id,
            Event.date >= db.func.current_timestamp()
        ).order_by(Event.date.asc()).limit(5).all()
        
        # Recent posts
        recent_posts = Post.query.filter(
            Post.community_id == community.id
        ).order_by(Post.created_at.desc()).limit(5).all()
        
        community_data = {
            'id': str(community.id),
            'name': community.name,
            'avatar': community.avatar,
            'members': len(community.followers),
            'isFollowing': is_following,
            'category': community.category,
            'description': community.description,
            'established': community.established,
            'tags': tags,
            'upcomingEvents': [{
                'id': str(event.id),
                'title': event.title,
                'date': event.date.isoformat()
            } for event in upcoming_events],
            'recentPosts': [{
                'id': str(post.id),
                'content': post.content,
                'timestamp': post.created_at.isoformat(),
                'likes': post.likes.count()
            } for post in recent_posts]
        }
        
        result.append(community_data)
    
    return jsonify({
        'communities': result,
        'page': page,
        'total_pages': communities.pages,
        'total_items': communities.total
    }), 200


@communities_bp.route('/api/communities/<int:community_id>/follow', methods=['POST'])
def toggle_follow(community_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    community = Community.query.get_or_404(community_id)
    user = User.query.get_or_404(user_id)
    
    # Kullanıcı zaten takip ediyor mu?
    is_following = user in community.followers
    
    if is_following:
        # Takibi kaldır
        community.followers.remove(user)
        db.session.commit()
        is_following = False
    else:
        # Takip et
        community.followers.append(user)
        db.session.commit()
        is_following = True
    
    members_count = len(community.followers)
    
    return jsonify({
        'isFollowing': is_following,
        'members': members_count
    }), 200