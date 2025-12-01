"""
upload_service.py
-----------------
Local file upload servisi - Medya dosyalarını sunucu üzerinde saklar.

Bu servis, kullanıcıların yüklediği görsel ve video dosyalarını güvenli bir şekilde
local disk'e kaydeder ve erişilebilir URL'ler döndürür.

Özellikler:
- Unique dosya isimleri (UUID) ile çakışmaları önler
- Dosya tipi validasyonu (image/video)
- Güvenli dosya kaydetme
- Kolay dosya silme

Desteklenen Formatlar:
- Görseller: JPG, JPEG, PNG, GIF, WEBP
- Videolar: MP4, MOV, AVI, MKV, WEBM
"""

import os
import uuid
from werkzeug.utils import secure_filename

# Konfigürasyon
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'image': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
    'video': {'mp4', 'mov', 'avi', 'mkv', 'webm'}
}

# Upload klasörünü oluştur (yoksa)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def get_file_extension(filename):
    """
    Dosya uzantısını döndürür.

    Args:
        filename (str): Dosya adı (örn: "photo.jpg")

    Returns:
        str: Dosya uzantısı (örn: "jpg"), yoksa boş string

    Example:
        >>> get_file_extension("photo.jpg")
        'jpg'
        >>> get_file_extension("video.MP4")
        'mp4'
    """
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


def allowed_file(filename, media_type):
    """
    Dosya uzantısının izin verilen listede olup olmadığını kontrol eder.

    Args:
        filename (str): Kontrol edilecek dosya adı
        media_type (str): 'image' veya 'video'

    Returns:
        bool: Dosya uzantısı izin verilenler listesindeyse True

    Example:
        >>> allowed_file("photo.jpg", "image")
        True
        >>> allowed_file("document.pdf", "image")
        False
    """
    ext = get_file_extension(filename)

    if media_type == 'image':
        return ext in ALLOWED_EXTENSIONS['image']
    elif media_type == 'video':
        return ext in ALLOWED_EXTENSIONS['video']

    return False


def save_file(file_data, original_filename):
    """
    Dosyayı local disk'e kaydeder ve erişim bilgilerini döndürür.

    Dosya adı çakışmalarını önlemek için UUID kullanır. Orijinal uzantı korunur.

    Args:
        file_data (bytes): Dosyanın binary verisi
        original_filename (str): Kullanıcının yüklediği orijinal dosya adı

    Returns:
        dict or None: Başarılıysa dosya bilgileri, hata varsa None
            {
                'url': str,              # Flask endpoint'i (örn: "/uploads/abc123.jpg")
                'filename': str,         # Kayıtlı dosya adı (örn: "abc123.jpg")
                'original_filename': str,# Orijinal dosya adı
                'filepath': str          # Tam dosya yolu
            }

    Example:
        >>> file_data = b"image content here"
        >>> result = save_file(file_data, "vacation.jpg")
        >>> print(result['url'])
        '/uploads/a1b2c3d4e5f6.jpg'
    """
    try:
        # Güvenli unique dosya adı oluştur
        ext = get_file_extension(original_filename)
        unique_filename = f"{uuid.uuid4().hex}.{ext}"

        # Tam dosya yolu
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Dosyayı binary mode'da yaz
        with open(filepath, 'wb') as f:
            f.write(file_data)

        # Flask'ın serve edeceği URL
        file_url = f"/uploads/{unique_filename}"

        return {
            'url': file_url,
            'filename': unique_filename,
            'original_filename': original_filename,
            'filepath': filepath
        }

    except Exception as e:
        print(f"[ERROR] File save failed: {e}")
        return None


def delete_file(filename):
    """
    Dosyayı local disk'ten siler.

    Args:
        filename (str): Silinecek dosyanın adı (unique filename)

    Returns:
        bool: Başarılı silme işleminde True, aksi halde False

    Example:
        >>> delete_file("a1b2c3d4e5f6.jpg")
        True
        >>> delete_file("nonexistent.jpg")
        False
    """
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(filepath):
            os.remove(filepath)
            return True

        return False

    except Exception as e:
        print(f"[ERROR] File delete failed: {e}")
        return False
