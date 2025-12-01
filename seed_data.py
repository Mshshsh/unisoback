# seed_data.py
from main import app, db
from models import User, Community, Post, Event, CommunityTag, Mentor, MentorExpertise, Conversation, Message
from datetime import datetime, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Test kullanıcıları
    user1 = User(name="Sezer", avatar="👨‍💻", email="sezer@test.com")
    user2 = User(name="Ahmet", avatar="👤", email="ahmet@test.com")
    user3 = User(name="Ayşe", avatar="👩‍🎓", email="ayse@test.com")
    db.session.add_all([user1, user2, user3])
    db.session.commit()
    
    # Test communities
    community1 = Community(
        name="Yazılım Kulübü", 
        avatar="💻", 
        description="Yazılım geliştirme topluluğu",
        category="Teknoloji",
        established="2020"
    )
    community2 = Community(
        name="Müzik Kulübü", 
        avatar="🎵", 
        description="Müzik severlerin buluşma noktası",
        category="Sanat",
        established="2019"
    )
    community3 = Community(
        name="Spor Kulübü", 
        avatar="⚽", 
        description="Spor etkinlikleri ve turnuvalar",
        category="Spor",
        established="2018"
    )
    community4 = Community(
        name="Robotik Kulübü", 
        avatar="🤖", 
        description="Robot tasarım ve yapım",
        category="Teknoloji",
        established="2021"
    )
    db.session.add_all([community1, community2, community3, community4])
    db.session.commit()
    
    # Community tags
    tags1 = [
        CommunityTag(community_id=community1.id, tag="Python"),
        CommunityTag(community_id=community1.id, tag="JavaScript"),
        CommunityTag(community_id=community1.id, tag="Web"),
        CommunityTag(community_id=community1.id, tag="Mobile"),
    ]
    tags2 = [
        CommunityTag(community_id=community2.id, tag="Gitar"),
        CommunityTag(community_id=community2.id, tag="Konser"),
        CommunityTag(community_id=community2.id, tag="Müzikal"),
    ]
    tags3 = [
        CommunityTag(community_id=community3.id, tag="Futbol"),
        CommunityTag(community_id=community3.id, tag="Basketbol"),
        CommunityTag(community_id=community3.id, tag="Voleybol"),
    ]
    db.session.add_all(tags1 + tags2 + tags3)
    db.session.commit()
    
    # Kullanıcıları communitylere ekle (members)
    community1.members.append(user1)
    community1.members.append(user2)
    community2.members.append(user1)
    community3.members.append(user1)
    
    # Kullanıcıları communitylere ekle (followers)
    community1.followers.extend([user1, user2, user3])
    community2.followers.extend([user1, user3])
    community3.followers.append(user1)
    community4.followers.append(user2)
    db.session.commit()
    
    # Test events
    event1 = Event(
        community_id=community1.id,
        title="Hackathon 2024",
        date=datetime.utcnow() + timedelta(days=7),
        time="10:00 - 18:00",
        location="Teknoloji Merkezi",
        image="🏆",
        description="Yıllık hackathon etkinliği",
        capacity=100
    )
    event2 = Event(
        community_id=community2.id,
        title="Konser Gecesi",
        date=datetime.utcnow() + timedelta(days=14),
        time="20:00 - 23:00",
        location="Kampüs Amfisi",
        image="🎸",
        description="Kampüs konseri",
        capacity=200
    )
    event3 = Event(
        community_id=community3.id,
        title="Futbol Turnuvası",
        date=datetime.utcnow() + timedelta(days=3),
        time="14:00 - 18:00",
        location="Spor Sahası",
        image="⚽",
        description="Fakülteler arası futbol turnuvası",
        capacity=150
    )
    event4 = Event(
        community_id=community1.id,
        title="AI Workshop",
        date=datetime.utcnow() + timedelta(days=10),
        time="15:00 - 17:00",
        location="Bilgisayar Lab",
        image="🤖",
        description="Yapay zeka workshop",
        capacity=50
    )
    db.session.add_all([event1, event2, event3, event4])
    db.session.commit()
    
    # Event interests
    event1.interested_users.extend([user1, user2, user3])
    event2.interested_users.append(user1)
    event3.interested_users.extend([user1, user2])
    db.session.commit()
    
    # Test posts
    post1 = Post(
        user_id=user2.id,
        community_id=community1.id,
        event_id=event1.id,
        content="Hackathon'a katılacak var mı? Ekip arkadaşı arıyorum!",
        type="event",
        media_type="image",
        media_url="https://images.unsplash.com/photo-1504384308090-c894fdcc538d"
    )
    post2 = Post(
        user_id=user1.id,
        community_id=community1.id,
        content="Yeni proje fikirlerimizi paylaşalım! React Native ile mobil uygulama geliştirmeyi düşünüyorum.",
        type="community"
    )
    post3 = Post(
        user_id=user2.id,
        community_id=community2.id,
        event_id=event2.id,
        content="Konser gecesi için biletler satışta! Kaçırmayın 🎵",
        type="event",
        media_type="video",
        media_url="https://www.w3schools.com/html/mov_bbb.mp4"
    )
    post4 = Post(
        user_id=user3.id,
        community_id=community3.id,
        event_id=event3.id,
        content="Futbol turnuvası başlıyor! Tüm fakülteler davetlidir.",
        type="event",
        media_type="image",
        media_url="https://images.unsplash.com/photo-1579952363873-27f3bade9f55"
    )
    post5 = Post(
        user_id=user1.id,
        community_id=community2.id,
        content="Bu hafta sonu stüdyoda kayıt yapacağız, dinlemeye gelmek isteyen var mı?",
        type="community",
        media_type="image",
        media_url="https://images.unsplash.com/photo-1598488035139-bdbb2231ce04"
    )
    db.session.add_all([post1, post2, post3, post4, post5])
    db.session.commit()
    
    print("[OK] Test verileri basariyla olusturuldu!")
    print(f"[INFO] Olusturulan veriler:")
    print(f"   - {User.query.count()} kullanici")
    print(f"   - {Community.query.count()} topluluk")
    print(f"   - {CommunityTag.query.count()} tag")
    print(f"   - {Event.query.count()} etkinlik")
    print(f"   - {Post.query.count()} gonderi")
    print(f"\n[USER] Test icin USER_ID: {user1.id} (Sezer)")

    # seed_data.py sonuna ekle (önceki kodların altına)

    # Test mentors
    mentor1 = Mentor(
        user_id=user2.id,
        title="Senior Software Engineer",
        company="Google",
        bio="Mobil uygulama geliştirme alanında 8+ yıl deneyim. Kariyer geçişi ve teknik mülakatlarda yardımcı olabilirim.",
        availability="available",
        rating=4.9,
        sessions_completed=127,
        response_time="2 saat içinde"
    )
    mentor2 = Mentor(
        user_id=user3.id,
        title="Product Manager",
        company="Microsoft",
        bio="Ürün yöneticiliğine geçiş yapmak isteyenlere rehberlik ediyorum. Roadmap ve stratejik düşünme konularında destekçiyim.",
        availability="available",
        rating=4.8,
        sessions_completed=94,
        response_time="4 saat içinde"
    )
    
    # Yeni kullanıcılar (mentor olacak)
    user4 = User(name="Zeynep Demir", avatar="👩‍🎨", email="zeynep@test.com")
    user5 = User(name="Can Öztürk", avatar="👨‍🔬", email="can@test.com")
    db.session.add_all([user4, user5])
    db.session.commit()
    
    mentor3 = Mentor(
        user_id=user4.id,
        title="Lead UX Designer",
        company="Amazon",
        bio="Tasarım kariyerinizi planlamak ve portfolio oluşturma konusunda deneyimlerimi paylaşmak isterim.",
        availability="busy",
        rating=5.0,
        sessions_completed=156,
        response_time="1 gün içinde"
    )
    mentor4 = Mentor(
        user_id=user5.id,
        title="Data Scientist",
        company="Netflix",
        bio="Veri bilimi ve makine öğrenmesi alanında kariyer yapmak isteyenlere yol gösteriyorum.",
        availability="available",
        rating=4.7,
        sessions_completed=83,
        response_time="3 saat içinde"
    )
    db.session.add_all([mentor1, mentor2, mentor3, mentor4])
    db.session.commit()
    
    # Mentor expertise
    expertise1 = [
        MentorExpertise(mentor_id=mentor1.id, skill="React Native"),
        MentorExpertise(mentor_id=mentor1.id, skill="TypeScript"),
        MentorExpertise(mentor_id=mentor1.id, skill="Mobile Dev"),
    ]
    expertise2 = [
        MentorExpertise(mentor_id=mentor2.id, skill="Product Strategy"),
        MentorExpertise(mentor_id=mentor2.id, skill="Agile"),
        MentorExpertise(mentor_id=mentor2.id, skill="User Research"),
    ]
    expertise3 = [
        MentorExpertise(mentor_id=mentor3.id, skill="UI/UX Design"),
        MentorExpertise(mentor_id=mentor3.id, skill="Figma"),
        MentorExpertise(mentor_id=mentor3.id, skill="Design Systems"),
    ]
    expertise4 = [
        MentorExpertise(mentor_id=mentor4.id, skill="Machine Learning"),
        MentorExpertise(mentor_id=mentor4.id, skill="Python"),
        MentorExpertise(mentor_id=mentor4.id, skill="Data Analysis"),
    ]
    db.session.add_all(expertise1 + expertise2 + expertise3 + expertise4)
    db.session.commit()
    
    # Mentor followers
    mentor2.followers.append(user1)
    db.session.commit()
    
    print(f"   - {Mentor.query.count()} mentor")
    print(f"   - {MentorExpertise.query.count()} expertise")

    # Test conversations and messages
    conv1 = Conversation(
        user1_id=user1.id,
        user2_id=user2.id,
        last_message_at=datetime.utcnow()
    )
    conv2 = Conversation(
        user1_id=user1.id,
        user2_id=user3.id,
        last_message_at=datetime.utcnow() - timedelta(hours=2)
    )
    conv3 = Conversation(
        user1_id=user2.id,
        user2_id=user3.id,
        last_message_at=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add_all([conv1, conv2, conv3])
    db.session.commit()

    # Messages for conv1
    msg1 = Message(
        conversation_id=conv1.id,
        sender_id=user1.id,
        content="Merhaba! Hackathon icin takim kurmak ister misin?",
        is_read=True,
        created_at=datetime.utcnow() - timedelta(hours=3)
    )
    msg2 = Message(
        conversation_id=conv1.id,
        sender_id=user2.id,
        content="Evet, harika olur! Hangi teknolojileri kullanmayi dusunuyorsun?",
        is_read=True,
        created_at=datetime.utcnow() - timedelta(hours=2, minutes=50)
    )
    msg3 = Message(
        conversation_id=conv1.id,
        sender_id=user1.id,
        content="React Native ve Flask ile bir mobil uygulama yapmayi dusunuyorum.",
        is_read=False,
        created_at=datetime.utcnow() - timedelta(minutes=30)
    )

    # Messages for conv2
    msg4 = Message(
        conversation_id=conv2.id,
        sender_id=user3.id,
        content="Muzik kulubu etkinligine gelecek misin?",
        is_read=True,
        created_at=datetime.utcnow() - timedelta(hours=3)
    )
    msg5 = Message(
        conversation_id=conv2.id,
        sender_id=user1.id,
        content="Kesinlikle! Saat kacta basliyordu?",
        is_read=True,
        created_at=datetime.utcnow() - timedelta(hours=2)
    )

    # Messages for conv3
    msg6 = Message(
        conversation_id=conv3.id,
        sender_id=user2.id,
        content="Mentorlugun icin tesekkurler!",
        is_read=False,
        created_at=datetime.utcnow() - timedelta(days=1)
    )

    db.session.add_all([msg1, msg2, msg3, msg4, msg5, msg6])
    db.session.commit()

    print(f"   - {Conversation.query.count()} conversation")
    print(f"   - {Message.query.count()} message")