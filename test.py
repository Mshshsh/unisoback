# test_social.py
import requests
import json

BASE_URL = "http://localhost:5000"
USER_ID = 1

def print_separator(title=""):
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)

# ========== COMMUNITIES TESTS ==========

def test_get_all_communities():
    print_separator("GET /api/communities - Tüm Topluluklar")
    response = requests.get(f"{BASE_URL}/api/communities?user_id={USER_ID}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Toplam: {data['total_items']} topluluk")
        for community in data['communities']:
            print(f"\n  {community['name']} {community['avatar']}")
            print(f"    Kategori: {community['category']}")
            print(f"    Üye: {community['members']}")
            print(f"    Takip: {'✅' if community['isFollowing'] else '❌'}")
            print(f"    Tags: {', '.join(community['tags'][:3])}")
    return response.json() if response.status_code == 200 else None

def test_get_communities_by_category():
    print_separator("GET /api/communities?category=Teknoloji")
    response = requests.get(f"{BASE_URL}/api/communities?user_id={USER_ID}&category=Teknoloji")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Teknoloji kategorisinde {data['total_items']} topluluk")

def test_search_communities():
    print_separator("GET /api/communities?search=yazılım")
    response = requests.get(f"{BASE_URL}/api/communities?user_id={USER_ID}&search=yazılım")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🔍 Arama sonucu: {data['total_items']} topluluk")

def test_follow_community(community_id):
    print_separator(f"POST /api/communities/{community_id}/follow")
    response = requests.post(
        f"{BASE_URL}/api/communities/{community_id}/follow",
        json={"user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Takip durumu: {data['isFollowing']}")
        print(f"   Üye sayısı: {data['members']}")

def test_unfollow_community(community_id):
    print_separator(f"POST /api/communities/{community_id}/follow (unfollow)")
    response = requests.post(
        f"{BASE_URL}/api/communities/{community_id}/follow",
        json={"user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Takip durumu: {data['isFollowing']}")
        print(f"   Üye sayısı: {data['members']}")

# ========== EVENTS TESTS ==========

def test_get_all_events():
    print_separator("GET /api/events - Tüm Etkinlikler")
    response = requests.get(f"{BASE_URL}/api/events?user_id={USER_ID}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Toplam: {data['total_items']} etkinlik")
        for event in data['events']:
            print(f"\n  {event['title']} {event['image']}")
            print(f"    Topluluk: {event['community']}")
            print(f"    Tarih: {event['date'][:10]} - {event['time']}")
            print(f"    Konum: {event['location']}")
            print(f"    İlgilenen: {event['interested']} kişi")
            print(f"    Durum: {'✅ İlgileniyorum' if event['isInterested'] else '❌'}")
    return response.json() if response.status_code == 200 else None

def test_get_interested_events():
    print_separator("GET /api/events?filter=interested")
    response = requests.get(f"{BASE_URL}/api/events?user_id={USER_ID}&filter=interested")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 İlgilendiğim etkinlikler: {data['total_items']}")

def test_search_events():
    print_separator("GET /api/events?search=hackathon")
    response = requests.get(f"{BASE_URL}/api/events?user_id={USER_ID}&search=hackathon")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🔍 Arama sonucu: {data['total_items']} etkinlik")

def test_interest_event(event_id):
    print_separator(f"POST /api/events/{event_id}/interest")
    response = requests.post(
        f"{BASE_URL}/api/events/{event_id}/interest",
        json={"user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ İlgi durumu: {data['isInterested']}")
        print(f"   İlgilenen: {data['interested']} kişi")

def test_uninterest_event(event_id):
    print_separator(f"POST /api/events/{event_id}/interest (uninterest)")
    response = requests.post(
        f"{BASE_URL}/api/events/{event_id}/interest",
        json={"user_id": USER_ID}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ İlgi durumu: {data['isInterested']}")
        print(f"   İlgilenen: {data['interested']} kişi")

# ========== MAIN ==========

if __name__ == "__main__":
    print("\n🚀 Campus Social API - Communities & Events Test\n")
    
    try:
        # COMMUNITIES
        communities_data = test_get_all_communities()
        test_get_communities_by_category()
        test_search_communities()
        
        if communities_data and communities_data['communities']:
            first_community = communities_data['communities'][0]['id']
            test_follow_community(first_community)
            test_unfollow_community(first_community)
        
        # EVENTS
        events_data = test_get_all_events()
        test_get_interested_events()
        test_search_events()
        
        if events_data and events_data['events']:
            first_event = events_data['events'][0]['id']
            test_interest_event(first_event)
            test_uninterest_event(first_event)
        
        print_separator("✅ Tüm testler tamamlandı!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Sunucuya bağlanılamadı!")
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")