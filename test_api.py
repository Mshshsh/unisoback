# test_api.py
import requests
import json

BASE_URL = 'http://localhost:5000'

# Test için renk kodları
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(test_name, status, response=None):
    status_color = Colors.GREEN if status == "PASS" else Colors.RED
    print(f"{status_color}[{status}]{Colors.END} {test_name}")
    if response:
        print(f"  Response: {json.dumps(response, indent=2)}\n")

def test_auth():
    print(f"\n{Colors.BLUE}=== AUTH TESTS ==={Colors.END}\n")

    # Test 1: Register
    print(f"{Colors.YELLOW}Test 1: Register new user{Colors.END}")
    import random
    test_email = f'test{random.randint(1000, 9999)}@example.com'
    response = requests.post(f'{BASE_URL}/api/auth/register', json={
        'name': 'Test User',
        'email': test_email,
        'password': 'test123'
    })
    if response.status_code == 201:
        data = response.json()
        token = data.get('token')
        user_id = data['user']['id']
        print_test("Register", "PASS", data)
    else:
        print_test("Register", "FAIL", response.json())
        return None, None

    # Test 2: Login
    print(f"{Colors.YELLOW}Test 2: Login{Colors.END}")
    response = requests.post(f'{BASE_URL}/api/auth/login', json={
        'email': test_email,
        'password': 'test123'
    })
    if response.status_code == 200:
        print_test("Login", "PASS", response.json())
    else:
        print_test("Login", "FAIL", response.json())

    # Test 3: Get current user
    print(f"{Colors.YELLOW}Test 3: Get current user{Colors.END}")
    response = requests.get(
        f'{BASE_URL}/api/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    if response.status_code == 200:
        print_test("Get current user", "PASS", response.json())
    else:
        print_test("Get current user", "FAIL", response.json())

    # Test 4: Update profile
    print(f"{Colors.YELLOW}Test 4: Update profile{Colors.END}")
    response = requests.put(
        f'{BASE_URL}/api/auth/update-profile',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Updated Test User'}
    )
    if response.status_code == 200:
        print_test("Update profile", "PASS", response.json())
    else:
        print_test("Update profile", "FAIL", response.json())

    return token, user_id


def test_posts(user_id):
    print(f"\n{Colors.BLUE}=== POST TESTS ==={Colors.END}\n")

    # Test 1: Create post
    print(f"{Colors.YELLOW}Test 1: Create post{Colors.END}")
    response = requests.post(f'{BASE_URL}/api/posts', json={
        'user_id': user_id,
        'content': 'This is a test post!',
        'type': 'text'
    })
    if response.status_code == 201:
        data = response.json()
        post_id = data['post']['id']
        print_test("Create post", "PASS", data)
    else:
        print_test("Create post", "FAIL", response.json())
        return None

    # Test 2: Get feed
    print(f"{Colors.YELLOW}Test 2: Get feed{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/feed?user_id={user_id}')
    if response.status_code == 200:
        print_test("Get feed", "PASS", response.json())
    else:
        print_test("Get feed", "FAIL", response.json())

    # Test 3: Like post
    print(f"{Colors.YELLOW}Test 3: Like post{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/posts/{post_id}/like',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Like post", "PASS", response.json())
    else:
        print_test("Like post", "FAIL", response.json())

    # Test 4: Unlike post
    print(f"{Colors.YELLOW}Test 4: Unlike post{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/posts/{post_id}/like',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Unlike post", "PASS", response.json())
    else:
        print_test("Unlike post", "FAIL", response.json())

    return post_id


def test_comments(user_id, post_id):
    print(f"\n{Colors.BLUE}=== COMMENT TESTS ==={Colors.END}\n")

    # Test 1: Create comment
    print(f"{Colors.YELLOW}Test 1: Create comment{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/posts/{post_id}/comments',
        json={
            'user_id': user_id,
            'content': 'This is a test comment!'
        }
    )
    if response.status_code == 201:
        data = response.json()
        comment_id = data['comment']['id']
        print_test("Create comment", "PASS", data)
    else:
        print_test("Create comment", "FAIL", response.json())
        return None

    # Test 2: Get comments
    print(f"{Colors.YELLOW}Test 2: Get comments{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/posts/{post_id}/comments')
    if response.status_code == 200:
        print_test("Get comments", "PASS", response.json())
    else:
        print_test("Get comments", "FAIL", response.json())

    # Test 3: Delete comment
    print(f"{Colors.YELLOW}Test 3: Delete comment{Colors.END}")
    response = requests.delete(
        f'{BASE_URL}/api/posts/{post_id}/comments/{comment_id}',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Delete comment", "PASS", response.json())
    else:
        print_test("Delete comment", "FAIL", response.json())

    return comment_id


def test_communities(user_id):
    print(f"\n{Colors.BLUE}=== COMMUNITY TESTS ==={Colors.END}\n")

    # Test 1: Get communities
    print(f"{Colors.YELLOW}Test 1: Get communities{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/communities?user_id={user_id}')
    if response.status_code == 200:
        data = response.json()
        community_id = data['communities'][0]['id'] if data['communities'] else None
        print_test("Get communities", "PASS", data)
    else:
        print_test("Get communities", "FAIL", response.json())
        return None

    if not community_id:
        print(f"{Colors.RED}No communities found to test{Colors.END}")
        return None

    # Test 2: Follow community
    print(f"{Colors.YELLOW}Test 2: Follow community{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/communities/{community_id}/follow',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Follow community", "PASS", response.json())
    else:
        print_test("Follow community", "FAIL", response.json())

    # Test 3: Unfollow community
    print(f"{Colors.YELLOW}Test 3: Unfollow community{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/communities/{community_id}/follow',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Unfollow community", "PASS", response.json())
    else:
        print_test("Unfollow community", "FAIL", response.json())

    # Test 4: Search communities
    print(f"{Colors.YELLOW}Test 4: Search communities{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/communities?user_id={user_id}&search=Tech')
    if response.status_code == 200:
        print_test("Search communities", "PASS", response.json())
    else:
        print_test("Search communities", "FAIL", response.json())

    return community_id


def test_events(user_id):
    print(f"\n{Colors.BLUE}=== EVENT TESTS ==={Colors.END}\n")

    # Test 1: Get events
    print(f"{Colors.YELLOW}Test 1: Get events{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/events?user_id={user_id}')
    if response.status_code == 200:
        data = response.json()
        event_id = data['events'][0]['id'] if data['events'] else None
        print_test("Get events", "PASS", data)
    else:
        print_test("Get events", "FAIL", response.json())
        return None

    if not event_id:
        print(f"{Colors.RED}No events found to test{Colors.END}")
        return None

    # Test 2: Show interest in event
    print(f"{Colors.YELLOW}Test 2: Show interest in event{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/events/{event_id}/interest',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Show interest", "PASS", response.json())
    else:
        print_test("Show interest", "FAIL", response.json())

    # Test 3: Remove interest
    print(f"{Colors.YELLOW}Test 3: Remove interest{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/events/{event_id}/interest',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Remove interest", "PASS", response.json())
    else:
        print_test("Remove interest", "FAIL", response.json())

    # Test 4: Get interested events
    print(f"{Colors.YELLOW}Test 4: Get interested events{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/events?user_id={user_id}&filter=interested')
    if response.status_code == 200:
        print_test("Get interested events", "PASS", response.json())
    else:
        print_test("Get interested events", "FAIL", response.json())

    return event_id


def test_mentors(user_id):
    print(f"\n{Colors.BLUE}=== MENTOR TESTS ==={Colors.END}\n")

    # Test 1: Get mentors
    print(f"{Colors.YELLOW}Test 1: Get mentors{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/mentors?user_id={user_id}')
    if response.status_code == 200:
        data = response.json()
        mentor_id = data['mentors'][0]['id'] if data['mentors'] else None
        print_test("Get mentors", "PASS", data)
    else:
        print_test("Get mentors", "FAIL", response.json())
        return None

    if not mentor_id:
        print(f"{Colors.RED}No mentors found to test{Colors.END}")
        return None

    # Test 2: Follow mentor
    print(f"{Colors.YELLOW}Test 2: Follow mentor{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/mentors/{mentor_id}/follow',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Follow mentor", "PASS", response.json())
    else:
        print_test("Follow mentor", "FAIL", response.json())

    # Test 3: Unfollow mentor
    print(f"{Colors.YELLOW}Test 3: Unfollow mentor{Colors.END}")
    response = requests.post(
        f'{BASE_URL}/api/mentors/{mentor_id}/follow',
        json={'user_id': user_id}
    )
    if response.status_code == 200:
        print_test("Unfollow mentor", "PASS", response.json())
    else:
        print_test("Unfollow mentor", "FAIL", response.json())

    # Test 4: Get available mentors
    print(f"{Colors.YELLOW}Test 4: Get available mentors{Colors.END}")
    response = requests.get(f'{BASE_URL}/api/mentors?user_id={user_id}&filter=available')
    if response.status_code == 200:
        print_test("Get available mentors", "PASS", response.json())
    else:
        print_test("Get available mentors", "FAIL", response.json())

    return mentor_id


def test_cleanup(user_id, post_id):
    print(f"\n{Colors.BLUE}=== CLEANUP ==={Colors.END}\n")

    # Delete test post
    if post_id:
        print(f"{Colors.YELLOW}Deleting test post{Colors.END}")
        response = requests.delete(
            f'{BASE_URL}/api/posts/{post_id}',
            json={'user_id': user_id}
        )
        if response.status_code == 200:
            print_test("Delete post", "PASS", response.json())
        else:
            print_test("Delete post", "FAIL", response.json())


def main():
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}  CAMPUS SOCIAL API - ENDPOINT TESTS{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")

    try:
        # Test health endpoint
        print(f"\n{Colors.YELLOW}Testing server connection...{Colors.END}")
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code == 200:
            print(f"{Colors.GREEN}[OK] Server is running{Colors.END}\n")
        else:
            print(f"{Colors.RED}[FAIL] Server not responding{Colors.END}\n")
            return

        # Run tests
        token, user_id = test_auth()
        if not user_id:
            print(f"{Colors.RED}Auth tests failed, stopping...{Colors.END}")
            return

        post_id = test_posts(user_id)
        if post_id:
            test_comments(user_id, post_id)

        test_communities(user_id)
        test_events(user_id)
        test_mentors(user_id)

        # Cleanup
        if post_id:
            test_cleanup(user_id, post_id)

        print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
        print(f"{Colors.GREEN}  ALL TESTS COMPLETED{Colors.END}")
        print(f"{Colors.GREEN}{'='*50}{Colors.END}\n")

    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}[ERROR] Could not connect to server at {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Make sure the Flask server is running (python main.py){Colors.END}\n")
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {str(e)}{Colors.END}\n")


if __name__ == '__main__':
    main()
