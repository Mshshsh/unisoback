# Campus Social API

Flask tabanlı kampüs sosyal medya uygulaması backend'i.

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Test verileri oluştur (opsiyonel)
python seed_data.py

# Sunucuyu başlat
python main.py
```

Sunucu `http://localhost:5000` adresinde çalışmaya başlayacaktır.

### 2. Test

Tüm endpoint'leri test etmek için:
```bash
python test_api.py
```

---

## 📋 API Endpoints

### Authentication
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `POST` | `/api/auth/register` | Yeni kullanıcı kaydı | ❌ |
| `POST` | `/api/auth/login` | Kullanıcı girişi | ❌ |
| `GET` | `/api/auth/me` | Mevcut kullanıcı bilgisi | ✅ |
| `PUT` | `/api/auth/update-profile` | Profil güncelleme | ✅ |

### Feed & Posts
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/feed` | Kullanıcı feed'i | ❌ |
| `POST` | `/api/posts` | Yeni post oluştur | ❌ |
| `DELETE` | `/api/posts/<post_id>` | Post sil | ✅ |
| `POST` | `/api/posts/<post_id>/like` | Post beğen/beğeniyi kaldır | ❌ |

### Comments
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/posts/<post_id>/comments` | Yorumları getir | ❌ |
| `POST` | `/api/posts/<post_id>/comments` | Yorum ekle | ❌ |
| `DELETE` | `/api/posts/<post_id>/comments/<comment_id>` | Yorum sil | ✅ |

### Communities
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/communities` | Toplulukları listele | ❌ |
| `POST` | `/api/communities/<community_id>/follow` | Takip et/bırak | ❌ |

### Events
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/events` | Etkinlikleri listele | ❌ |
| `POST` | `/api/events/<event_id>/interest` | İlgi göster/kaldır | ❌ |

### Mentors
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/mentors` | Mentorları listele | ❌ |
| `POST` | `/api/mentors/<mentor_id>/follow` | Takip et/bırak | ❌ |

### Messages
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `GET` | `/api/conversations` | Tüm konuşmalar | ❌ |
| `POST` | `/api/conversations` | Yeni konuşma başlat | ❌ |
| `GET` | `/api/conversations/<id>/messages` | Mesajları getir | ❌ |
| `POST` | `/api/conversations/<id>/messages` | Mesaj gönder | ❌ |
| `PUT` | `/api/messages/<id>/read` | Okundu işaretle | ❌ |
| `DELETE` | `/api/conversations/<id>` | Konuşmayı sil | ❌ |

### Upload (Medya Dosyaları)
| Method | Endpoint | Açıklama | Auth |
|--------|----------|----------|------|
| `POST` | `/api/upload` | Dosya yükle (image/video) | ❌ |
| `DELETE` | `/api/upload/<filename>` | Dosya sil | ❌ |
| `GET` | `/uploads/<filename>` | Dosyaya erişim | ❌ |

**Desteklenen Formatlar:**
- Görseller: JPG, JPEG, PNG, GIF, WEBP
- Videolar: MP4, MOV, AVI, MKV, WEBM
- Maksimum Boyut: 20MB

---

## 💡 Örnek Kullanım

### Kullanıcı Kaydı
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ahmet Yılmaz",
    "email": "ahmet@example.com",
    "password": "securepass123"
  }'
```

### Kullanıcı Girişi
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ahmet@example.com",
    "password": "securepass123"
  }'
```

### Dosya Yükleme
```bash
# 1. Dosyayı yükle
curl -X POST http://localhost:5000/api/upload \
  -F "file=@photo.jpg" \
  -F "media_type=image"

# Response:
# {
#   "message": "Dosya basariyla yuklendi",
#   "media_url": "/uploads/abc123def456.jpg",
#   "filename": "abc123def456.jpg",
#   "media_type": "image"
# }
```

### Medya ile Post Oluşturma
```bash
# 2. Yüklenen dosya ile post oluştur
curl -X POST http://localhost:5000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "content": "Yeni fotoğrafım!",
    "type": "text",
    "media_type": "image",
    "media_url": "http://localhost:5000/uploads/abc123def456.jpg"
  }'
```

### Feed Getirme
```bash
curl "http://localhost:5000/api/feed?user_id=1&page=1&limit=10"
```

### Post Beğenme
```bash
curl -X POST http://localhost:5000/api/posts/1/like \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

### Yorum Ekleme
```bash
curl -X POST http://localhost:5000/api/posts/1/comments \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "content": "Harika bir gönderi!"
  }'
```

---

## 🗄️ Veritabanı Modelleri

- **User** - Kullanıcı bilgileri
- **Community** - Topluluk bilgileri
- **Event** - Etkinlik bilgileri
- **Post** - Gönderiler (text, image, video destekli)
- **PostLike** - Post beğenileri
- **Comment** - Post yorumları
- **Mentor** - Mentor profilleri
- **MentorExpertise** - Mentor uzmanlık alanları
- **CommunityTag** - Topluluk etiketleri
- **Conversation** - Mesajlaşma konuşmaları
- **Message** - Mesajlar

---

## ✨ Özellikler

- ✅ **JWT Authentication** - Güvenli kullanıcı doğrulama
- ✅ **RESTful API** - Standart HTTP metodları
- ✅ **SQLite Database** - Hafif ve hızlı veritabanı
- ✅ **CORS Support** - Cross-origin istekleri destekler
- ✅ **Pagination** - Sayfalama desteği
- ✅ **File Upload** - Local medya dosyası yükleme
- ✅ **Many-to-many Relationships** - İlişkisel veri yapıları
- ✅ **Cascade Deletes** - Otomatik bağlantılı silme
- ✅ **Input Validation** - Veri doğrulama
- ✅ **Authorization Checks** - Yetkilendirme kontrolleri

---

## 🛠️ Teknolojiler

- **Flask** 3.0.0 - Web framework
- **Flask-SQLAlchemy** 3.1.1 - ORM
- **Flask-CORS** 4.0.0 - CORS desteği
- **PyJWT** 2.8.0 - JWT token yönetimi
- **SQLite** - Veritabanı
- **Werkzeug** 3.0.1 - WSGI utilities

---

## 📁 Proje Yapısı

```
unisoback/
├── main.py                 # Flask uygulaması ve konfigürasyon
├── models.py               # Database modelleri
├── upload_service.py       # Dosya upload servisi
│
├── routes/
│   ├── auth.py            # Authentication endpoints
│   ├── feed.py            # Feed & Posts endpoints
│   ├── communities.py     # Communities endpoints
│   ├── events.py          # Events endpoints
│   ├── mentors.py         # Mentors endpoints
│   ├── messages.py        # Messaging endpoints
│   └── upload.py          # File upload endpoints
│
├── uploads/               # Yüklenen medya dosyaları (gitignore)
├── campus.db              # SQLite veritabanı (gitignore)
│
├── seed_data.py           # Test verileri oluşturma scripti
├── test_api.py            # API test scripti
├── test_upload.py         # Upload test scripti
│
├── requirements.txt       # Python bağımlılıkları
├── .gitignore            # Git ignore kuralları
└── README.md             # Bu dosya
```
