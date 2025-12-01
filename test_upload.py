# test_upload.py
import requests

BASE_URL = 'http://localhost:5000'

print("\n=== LOCAL UPLOAD TEST ===\n")

# Test dosyası oluştur
test_content = b"Test image content for local upload"
with open('test_upload_file.jpg', 'wb') as f:
    f.write(test_content)

print("[1] Test dosyasi olusturuldu")

# Upload testi
print("\n[2] Dosya yukleniyor...")
with open('test_upload_file.jpg', 'rb') as f:
    files = {'file': ('test_upload_file.jpg', f, 'image/jpeg')}
    data = {'media_type': 'image'}

    response = requests.post(f'{BASE_URL}/api/upload', files=files, data=data)

    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n[OK] Dosya basariyla yuklendi!")
        print(f"  Media URL: {result['media_url']}")
        print(f"  Filename: {result['filename']}")
        print(f"  Full URL: {BASE_URL}{result['media_url']}")

        # Post oluşturma testi
        print("\n[3] Post olusturuluyor...")
        post_response = requests.post(f'{BASE_URL}/api/posts', json={
            'user_id': 1,
            'content': 'Test post with local uploaded image',
            'type': 'text',
            'media_type': result['media_type'],
            'media_url': f"{BASE_URL}{result['media_url']}"
        })

        print(f"Status Code: {post_response.status_code}")
        if post_response.status_code == 201:
            post_data = post_response.json()
            print(f"Response: {post_response.json()}")
            print("\n[OK] Post basariyla olusturuldu!")
            print(f"  Post ID: {post_data['post']['id']}")
        else:
            print(f"Response: {post_response.json()}")
            print("\n[FAIL] Post olusturulamadi")

    else:
        print("\n[FAIL] Dosya yuklenemedi")

print("\n=== TEST TAMAMLANDI ===\n")
