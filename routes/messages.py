# routes/messages.py
from flask import Blueprint, jsonify, request
from models import db, Conversation, Message, User
from sqlalchemy import or_, and_

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/api/conversations', methods=['GET'])
def get_conversations():
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    # Kullanıcının tüm konuşmalarını getir
    conversations = Conversation.query.filter(
        or_(
            Conversation.user1_id == user_id,
            Conversation.user2_id == user_id
        )
    ).order_by(Conversation.last_message_at.desc()).all()

    result = []
    for conv in conversations:
        # Diğer kullanıcıyı bul
        other_user = conv.user2 if conv.user1_id == user_id else conv.user1

        # Son mesajı al
        last_message = conv.messages.order_by(Message.created_at.desc()).first()

        # Okunmamış mesaj sayısını hesapla
        unread_count = conv.messages.filter(
            and_(
                Message.sender_id != user_id,
                Message.is_read == False
            )
        ).count()

        conv_data = {
            'id': str(conv.id),
            'otherUser': {
                'id': str(other_user.id),
                'name': other_user.name,
                'avatar': other_user.avatar
            },
            'lastMessage': {
                'content': last_message.content,
                'timestamp': last_message.created_at.isoformat(),
                'senderId': str(last_message.sender_id)
            } if last_message else None,
            'unreadCount': unread_count,
            'lastMessageAt': conv.last_message_at.isoformat() if conv.last_message_at else conv.created_at.isoformat()
        }

        result.append(conv_data)

    return jsonify({
        'conversations': result
    }), 200


@messages_bp.route('/api/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 50, type=int)

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    conversation = Conversation.query.get_or_404(conversation_id)

    # Kullanıcının bu konuşmaya erişimi var mı kontrol et
    if conversation.user1_id != user_id and conversation.user2_id != user_id:
        return jsonify({'error': 'Bu konuşmaya erişim yetkiniz yok'}), 403

    # Mesajları getir
    messages = Message.query.filter_by(
        conversation_id=conversation_id
    ).order_by(Message.created_at.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )

    # Okunmamış mesajları okundu olarak işaretle
    unread_messages = Message.query.filter(
        and_(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False
        )
    ).all()

    for msg in unread_messages:
        msg.is_read = True
    db.session.commit()

    result = []
    for msg in messages.items:
        msg_data = {
            'id': str(msg.id),
            'content': msg.content,
            'senderId': str(msg.sender_id),
            'isRead': msg.is_read,
            'timestamp': msg.created_at.isoformat(),
            'sender': {
                'id': str(msg.sender.id),
                'name': msg.sender.name,
                'avatar': msg.sender.avatar
            }
        }
        result.append(msg_data)

    return jsonify({
        'messages': list(reversed(result)),  # En eski mesaj en üstte
        'page': page,
        'total_pages': messages.pages,
        'total_items': messages.total
    }), 200


@messages_bp.route('/api/conversations', methods=['POST'])
def create_or_get_conversation():
    data = request.get_json()
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')

    if not user1_id or not user2_id:
        return jsonify({'error': 'user1_id ve user2_id gerekli'}), 400

    if user1_id == user2_id:
        return jsonify({'error': 'Kendinizle konuşma başlatamazsınız'}), 400

    # Kullanıcılar var mı kontrol et
    user1 = User.query.get_or_404(user1_id)
    user2 = User.query.get_or_404(user2_id)

    # Mevcut konuşmayı kontrol et
    existing_conv = Conversation.query.filter(
        or_(
            and_(Conversation.user1_id == user1_id, Conversation.user2_id == user2_id),
            and_(Conversation.user1_id == user2_id, Conversation.user2_id == user1_id)
        )
    ).first()

    if existing_conv:
        return jsonify({
            'conversation': {
                'id': str(existing_conv.id),
                'created': False
            }
        }), 200

    # Yeni konuşma oluştur
    new_conv = Conversation(
        user1_id=user1_id,
        user2_id=user2_id
    )

    db.session.add(new_conv)
    db.session.commit()

    return jsonify({
        'conversation': {
            'id': str(new_conv.id),
            'created': True
        }
    }), 201


@messages_bp.route('/api/conversations/<int:conversation_id>/messages', methods=['POST'])
def send_message(conversation_id):
    data = request.get_json()
    sender_id = data.get('sender_id')
    content = data.get('content')

    if not sender_id:
        return jsonify({'error': 'sender_id gerekli'}), 400

    if not content or not content.strip():
        return jsonify({'error': 'content gerekli'}), 400

    conversation = Conversation.query.get_or_404(conversation_id)

    # Kullanıcının bu konuşmaya erişimi var mı kontrol et
    if conversation.user1_id != sender_id and conversation.user2_id != sender_id:
        return jsonify({'error': 'Bu konuşmaya mesaj gönderme yetkiniz yok'}), 403

    sender = User.query.get_or_404(sender_id)

    # Yeni mesaj oluştur
    new_message = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        content=content.strip()
    )

    db.session.add(new_message)

    # Konuşmanın son mesaj zamanını güncelle
    conversation.last_message_at = new_message.created_at
    db.session.commit()

    return jsonify({
        'message': 'Mesaj gonderildi',
        'data': {
            'id': str(new_message.id),
            'content': new_message.content,
            'senderId': str(new_message.sender_id),
            'isRead': new_message.is_read,
            'timestamp': new_message.created_at.isoformat(),
            'sender': {
                'id': str(sender.id),
                'name': sender.name,
                'avatar': sender.avatar
            }
        }
    }), 201


@messages_bp.route('/api/messages/<int:message_id>/read', methods=['PUT'])
def mark_as_read(message_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    message = Message.query.get_or_404(message_id)

    # Sadece mesajın alıcısı işaretleyebilir
    if message.sender_id == user_id:
        return jsonify({'error': 'Kendi mesajinizi okudu olarak isaretleyemezsiniz'}), 403

    message.is_read = True
    db.session.commit()

    return jsonify({
        'message': 'Mesaj okundu olarak isaretlendi'
    }), 200


@messages_bp.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'user_id gerekli'}), 400

    conversation = Conversation.query.get_or_404(conversation_id)

    # Sadece konuşmanın bir parçası olan kullanıcı silebilir
    if conversation.user1_id != user_id and conversation.user2_id != user_id:
        return jsonify({'error': 'Bu konusmayi silme yetkiniz yok'}), 403

    db.session.delete(conversation)
    db.session.commit()

    return jsonify({
        'message': 'Konusma silindi'
    }), 200
