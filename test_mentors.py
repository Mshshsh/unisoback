# test_mentors.py
import requests
import json

BASE_URL = "http://localhost:5000"
USER_ID = 1

def print_separator(title=""):
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)

def get_availability_emoji(availability):
    if availability == 'available':
        return '🟢'
    elif availability == 'busy':
        return '🟡'
    else:
        return '⚫'

def test_get_all_mentors():
    print_separator("GET /api/mentors - Tüm Mentorlar")
    response = requests.get(f"{BASE_URL}/api/mentors?user_id={USER_ID}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Toplam: {data['total_items']} mentor")
        for mentor in data['mentors']:
            print(f"\n  {mentor['name']} {mentor['avatar']}")
            print(f"    {mentor['title']} @ {mentor['company']}")
            print(f"    {get_availability_emoji(mentor['availability'])} {mentor['availability']}")
            print(f"    ⭐ {mentor['rating']} | ✅ {mentor['sessionsCompleted']} seans")
            print(f"    💬 Yanıt süresi: {mentor['responseTime']}")
            print(f"    🎯 Uzmanlık: {', '.join(mentor['expertise'][:3])}")
            print(f"    Takip: {'✅' if mentor['isFollowing'] else '❌'}")
    return response.json() if response.status_code == 200 else None

def test_get_available_mentors():
    print_separator("GET /api/mentors?filter=available")
    response = requests.get(f"{BASE_URL}/api/mentors?user_id={USER_ID}&filter=available")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Müsait mentorlar: {data['total_items']}")

def test_get_following_mentors():
    print_separator("GET /api/mentors?filter=following")
    response = requests.get(f"{BASE_URL}/api/mentors?user_id={USER_ID}&filter=following")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Takip edilen mentorlar: {data['total_items']}")

def test_follow_mentor(mentor_id):
    print_separator(f"POST /api/mentors/{mentor_id}/follow")
    response = requests.post(
        f"{BASE_URL}/api/mentors/{mentor_id}/follow",
        json={"user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Takip durumu: {data['isFollowing']}")

def test_unfollow_mentor(mentor_id):
    print_separator(f"POST /api/mentors/{mentor_id}/follow (unfollow)")
    response = requests.post(
        f"{BASE_URL}/api/mentors/{mentor_id}/follow",
        json={"user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Takip durumu: {data['isFollowing']}")

if __name__ == "__main__":
    print("\n🚀 Campus Social API - Mentors Test\n")
    
    try:
        # Mentorları getir
        mentors_data = test_get_all_mentors()
        test_get_available_mentors()
        test_get_following_mentors()
        
        if mentors_data and mentors_data['mentors']:
            first_mentor = mentors_data['mentors'][0]['id']
            test_follow_mentor(first_mentor)
            test_unfollow_mentor(first_mentor)
        
        print_separator("✅ Tüm testler tamamlandı!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Sunucuya bağlanılamadı!")
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")