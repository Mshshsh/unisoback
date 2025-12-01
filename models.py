# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Community-User many-to-many ilişkisi (members)
community_members = db.Table('community_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id'))
)

# Community-User many-to-many ilişkisi (followers)
community_followers = db.Table('community_followers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

# Event-User many-to-many ilişkisi (interests)
event_interests = db.Table('event_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

# Mentor-User many-to-many ilişkisi (followers)
mentor_followers = db.Table('mentor_followers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('mentor_id', db.Integer, db.ForeignKey('mentors.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    department = db.Column(db.String(100))
    year = db.Column(db.Integer)
    age = db.Column(db.Integer)
    interests = db.Column(db.Text)  # JSON string olarak saklanacak
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Community(db.Model):
    __tablename__ = 'communities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    established = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    members = db.relationship('User', secondary=community_members, backref='communities')
    followers = db.relationship('User', secondary=community_followers, backref='following_communities')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(50))
    location = db.Column(db.String(200))
    image = db.Column(db.String(200))
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    community = db.relationship('Community', backref='events')
    interested_users = db.relationship('User', secondary=event_interests, backref='interested_events')

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    media_type = db.Column(db.String(20))  # 'image', 'video', None
    media_url = db.Column(db.String(500))  # URL veya path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref='posts')
    community = db.relationship('Community', backref='posts')
    event = db.relationship('Event', backref='posts')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref='comments')
    post_ref = db.relationship('Post', backref='comments')

class CommunityTag(db.Model):
    __tablename__ = 'community_tags'
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    
    community = db.relationship('Community', backref='tags')

class Mentor(db.Model):
    __tablename__ = 'mentors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text)
    availability = db.Column(db.String(20), default='available')  # available, busy, offline
    rating = db.Column(db.Float, default=0.0)
    sessions_completed = db.Column(db.Integer, default=0)
    response_time = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='mentor_profile')
    followers = db.relationship('User', secondary=mentor_followers, backref='following_mentors')

class MentorExpertise(db.Model):
    __tablename__ = 'mentor_expertise'
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False)
    skill = db.Column(db.String(100), nullable=False)

    mentor = db.relationship('Mentor', backref='expertise')

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user1 = db.relationship('User', foreign_keys=[user1_id], backref='conversations_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='conversations_as_user2')
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', backref='sent_messages')