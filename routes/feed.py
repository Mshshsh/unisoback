# routes/feed.py
from flask import Blueprint, jsonify, request
from models import db, Post, PostLike, Comment, User, Community, Event

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/api/feed', methods=['GET'])
def get_feed():
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400
    
    # Kullanıcının takip ettiği toplulukların postlarını getir
    posts = Post.query.join(Community).filter(
        Community.members.any(id=user_id)
    ).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )
    
    result = []
    for post in posts.items:
        # Kullanıcının bu postu beğenip beğenmediğini kontrol et
        is_liked = PostLike.query.filter_by(
            post_id=post.id, 
            user_id=user_id
        ).first() is not None
        
        post_data = {
            'id': str(post.id),
            'type': post.type,
            'author': {
                'name': post.author.name,
                'avatar': post.author.avatar
            },
            'content': post.content,
            'timestamp': post.created_at.isoformat(),
            'likes': post.likes.count(),
            'isLiked': is_liked,
            'mediaType': post.media_type,
            'mediaUrl': post.media_url
        }

        if post.community:
            post_data['community'] = {
                'id': str(post.community.id),
                'name': post.community.name,
                'avatar': post.community.avatar
            }
        
        if post.event:
            post_data['event'] = {
                'id': str(post.event.id),
                'title': post.event.title,
                'date': post.event.date.isoformat(),
                'image': post.event.image
            }
        
        result.append(post_data)
    
    return jsonify({
        'posts': result,
        'page': page,
        'total_pages': posts.pages,
        'total_items': posts.total
    }), 200


@feed_bp.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    post_type = data.get('type', 'text')  # 'text', 'event', 'announcement'
    community_id = data.get('community_id')
    event_id = data.get('event_id')
    media_type = data.get('media_type')  # 'image', 'video', None
    media_url = data.get('media_url')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    if not content:
        return jsonify({'error': 'content gerekli'}), 400

    # Kullanıcının var olduğunu kontrol et
    user = User.query.get_or_404(user_id)

    # Yeni post oluştur
    new_post = Post(
        user_id=user_id,
        content=content,
        type=post_type,
        community_id=community_id,
        event_id=event_id,
        media_type=media_type,
        media_url=media_url
    )

    db.session.add(new_post)
    db.session.commit()

    # Oluşturulan postu döndür
    post_data = {
        'id': str(new_post.id),
        'type': new_post.type,
        'author': {
            'name': user.name,
            'avatar': user.avatar
        },
        'content': new_post.content,
        'timestamp': new_post.created_at.isoformat(),
        'likes': 0,
        'isLiked': False,
        'mediaType': new_post.media_type,
        'mediaUrl': new_post.media_url
    }

    if new_post.community:
        post_data['community'] = {
            'id': str(new_post.community.id),
            'name': new_post.community.name,
            'avatar': new_post.community.avatar
        }

    if new_post.event:
        post_data['event'] = {
            'id': str(new_post.event.id),
            'title': new_post.event.title,
            'date': new_post.event.date.isoformat(),
            'image': new_post.event.image
        }

    return jsonify({
        'message': 'Post başarıyla oluşturuldu',
        'post': post_data
    }), 201


@feed_bp.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    post = Post.query.get_or_404(post_id)

    # Sadece post sahibi silebilir
    if post.user_id != user_id:
        return jsonify({'error': 'Bu postu silme yetkiniz yok'}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        'message': 'Post başarıyla silindi'
    }), 200


@feed_bp.route('/api/posts/<int:post_id>/like', methods=['POST'])
def toggle_like(post_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    post = Post.query.get_or_404(post_id)
    existing_like = PostLike.query.filter_by(
        post_id=post_id,
        user_id=user_id
    ).first()

    if existing_like:
        # Beğeniyi kaldır
        db.session.delete(existing_like)
        db.session.commit()
        is_liked = False
    else:
        # Beğeni ekle
        new_like = PostLike(post_id=post_id, user_id=user_id)
        db.session.add(new_like)
        db.session.commit()
        is_liked = True

    likes_count = post.likes.count()

    return jsonify({
        'likes': likes_count,
        'isLiked': is_liked
    }), 200


@feed_bp.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    post = Post.query.get_or_404(post_id)

    comments = Comment.query.filter_by(post_id=post_id).order_by(
        Comment.created_at.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    result = []
    for comment in comments.items:
        comment_data = {
            'id': str(comment.id),
            'content': comment.content,
            'timestamp': comment.created_at.isoformat(),
            'author': {
                'id': str(comment.author.id),
                'name': comment.author.name,
                'avatar': comment.author.avatar
            }
        }
        result.append(comment_data)

    return jsonify({
        'comments': result,
        'page': page,
        'total_pages': comments.pages,
        'total_items': comments.total
    }), 200


@feed_bp.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    if not content:
        return jsonify({'error': 'content gerekli'}), 400

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)

    new_comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=content
    )

    db.session.add(new_comment)
    db.session.commit()

    comment_data = {
        'id': str(new_comment.id),
        'content': new_comment.content,
        'timestamp': new_comment.created_at.isoformat(),
        'author': {
            'id': str(user.id),
            'name': user.name,
            'avatar': user.avatar
        }
    }

    return jsonify({
        'message': 'Yorum başarıyla eklendi',
        'comment': comment_data
    }), 201


@feed_bp.route('/api/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    comment = Comment.query.get_or_404(comment_id)

    # Sadece yorum sahibi silebilir
    if comment.user_id != user_id:
        return jsonify({'error': 'Bu yorumu silme yetkiniz yok'}), 403

    if comment.post_id != post_id:
        return jsonify({'error': 'Yorum bu posta ait değil'}), 400

    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        'message': 'Yorum başarıyla silindi'
    }), 200
