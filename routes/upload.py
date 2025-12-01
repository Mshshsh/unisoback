"""
routes/upload.py
----------------
Medya dosyası yükleme API endpoint'leri.

Bu modül, kullanıcıların görsel ve video dosyalarını yüklemesi ve silmesi
için gerekli REST API endpoint'lerini sağlar.

Endpoints:
- POST   /api/upload         - Yeni dosya yükle
- DELETE /api/upload/<filename> - Dosya sil

Maksimum Dosya Boyutu: 20MB
"""

from flask import Blueprint, jsonify, request
from upload_service import save_file, delete_file, allowed_file
import os

upload_bp = Blueprint('upload', __name__)

# Konfigürasyon
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


@upload_bp.route('/api/upload', methods=['POST'])
def upload_media():
    """
    Medya dosyası yükler (görsel veya video).

    Request (multipart/form-data):
        file: Dosya binary data
        media_type: 'image' veya 'video'

    Response (200 OK):
        {
            "message": "Dosya basariyla yuklendi",
            "media_url": "/uploads/abc123.jpg",
            "filename": "abc123.jpg",
            "media_type": "image"
        }

    Error Responses:
        400: Dosya bulunamadı / Geçersiz tip / Dosya boş
        413: Dosya çok büyük (>20MB)
        500: Upload hatası

    Example:
        curl -X POST http://localhost:5000/api/upload \\
             -F "file=@photo.jpg" \\
             -F "media_type=image"
    """
    # 1. Dosya varlık kontrolü
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadi'}), 400

    file = request.files['file']
    media_type = request.form.get('media_type', 'image')

    if file.filename == '':
        return jsonify({'error': 'Dosya secilmedi'}), 400

    # 2. Dosya tipi validasyonu
    if not allowed_file(file.filename, media_type):
        return jsonify({
            'error': f'Gecersiz dosya tipi. Lutfen {media_type} dosyasi yukleyin'
        }), 400

    # 3. Dosya boyutu kontrolü
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Pozisyonu başa al

    if file_size > MAX_FILE_SIZE:
        max_size_mb = MAX_FILE_SIZE / 1024 / 1024
        return jsonify({
            'error': f'Dosya boyutu cok buyuk. Maksimum: {max_size_mb:.0f}MB'
        }), 400

    if file_size == 0:
        return jsonify({'error': 'Dosya bos'}), 400

    # 4. Dosyayı kaydet
    try:
        file_data = file.read()
        result = save_file(file_data, file.filename)

        if not result:
            return jsonify({'error': 'Dosya yukleme basarisiz'}), 500

        # Başarılı response
        return jsonify({
            'message': 'Dosya basariyla yuklendi',
            'media_url': result['url'],
            'filename': result['filename'],
            'media_type': media_type
        }), 200

    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return jsonify({'error': 'Dosya yukleme sirasinda hata olustu'}), 500


@upload_bp.route('/api/upload/<filename>', methods=['DELETE'])
def delete_media(filename):
    """
    Yüklenmiş dosyayı siler.

    URL Parameters:
        filename: Silinecek dosyanın adı (unique filename)

    Response (200 OK):
        {
            "message": "Dosya basariyla silindi"
        }

    Error Responses:
        404: Dosya bulunamadı
        500: Silme hatası

    Example:
        curl -X DELETE http://localhost:5000/api/upload/abc123.jpg

    Security Note:
        Production'da bu endpoint için authorization kontrolü eklenmelidir.
        Sadece dosya sahibi kendi dosyasını silebilmeli.
    """
    try:
        success = delete_file(filename)

        if success:
            return jsonify({'message': 'Dosya basariyla silindi'}), 200
        else:
            return jsonify({'error': 'Dosya bulunamadi veya silinemedi'}), 404

    except Exception as e:
        print(f"[ERROR] Delete failed: {e}")
        return jsonify({'error': 'Dosya silme sirasinda hata olustu'}), 500
