import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test 1: Register User1
print("=== Test 1: Register User1 ===")
user1_data = {
    "email": "user1@example.com",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/auth/register", json=user1_data)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")
user1_token = response.json().get("access_token") if response.status_code == 201 else None

if response.status_code != 201:
    print("Failed to register user1. Aborting tests.")
    exit(1)

# Test 2: Login User1
print("\n=== Test 2: Login User1 ===")
login_data = {
    "email": "user1@example.com",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")
user1_token = response.json().get("access_token") if response.status_code == 200 else user1_token

# Test 3: Get Current User (ME)
print("\n=== Test 3: Get Current User ===")
headers = {"Authorization": f"Bearer {user1_token}"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")

# Test 4: Create a Todo for User1
print("\n=== Test 4: Create Todo for User1 ===")
todo_data = {
    "title": "User1 Todo",
    "description": "This is a todo for user 1"
}
response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")

# Test 5: Get User1's Todos
print("\n=== Test 5: Get User1's Todos ===")
response = requests.get(f"{BASE_URL}/todos", headers=headers)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")

# Test 6: Register User2
print("\n=== Test 6: Register User2 ===")
user2_data = {
    "email": "user2@example.com",
    "password": "password456"
}
response = requests.post(f"{BASE_URL}/auth/register", json=user2_data)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")
user2_token = response.json().get("access_token") if response.status_code == 201 else None

# Test 7: Login User2
print("\n=== Test 7: Login User2 ===")
login_data = {
    "email": "user2@example.com",
    "password": "password456"
}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")
user2_token = response.json().get("access_token") if response.status_code == 200 else user2_token

# Test 8: Try to access User1's Todos with User2's Token (Should fail)
print("\n=== Test 8: User2 Try to Get User1's Todos (Should Fail) ===")
user2_headers = {"Authorization": f"Bearer {user2_token}"}
response = requests.get(f"{BASE_URL}/todos", headers=user2_headers)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")
print(f"Expected: User2 should see 0 todos (not User1's)")

# Test 9: User2 Create Own Todo
print("\n=== Test 9: User2 Create Own Todo ===")
todo_data = {
    "title": "User2 Todo",
    "description": "This is a todo for user 2"
}
response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=user2_headers)
print(f"Status: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Response Text: {response.text}")

# Test 10: Verification - User1 and User2 See Different Todos
print("\n=== Test 10: Verify User Isolation ===")
print("User1's Todos:")
response = requests.get(f"{BASE_URL}/todos", headers=headers)
try:
    user1_todos = response.json().get("items", [])
except:
    print(f"Error getting user1 todos: {response.text}")
    user1_todos = []
print(f"Count: {len(user1_todos)}, Titles: {[t['title'] for t in user1_todos]}")

print("User2's Todos:")
response = requests.get(f"{BASE_URL}/todos", headers=user2_headers)
try:
    user2_todos = response.json().get("items", [])
except:
    print(f"Error getting user2 todos: {response.text}")
    user2_todos = []
print(f"Count: {len(user2_todos)}, Titles: {[t['title'] for t in user2_todos]}")

if len(user1_todos) == 1 and len(user2_todos) == 1:
    print("\n[PASS] USER ISOLATION WORKING! User1 and User2 have separate todos")
else:
    print(f"\n[FAIL] ISOLATION PROBLEM: User1 has {len(user1_todos)}, User2 has {len(user2_todos)}")
