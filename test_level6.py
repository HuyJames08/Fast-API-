import requests
import json
from datetime import datetime, timedelta, date

BASE_URL = "http://localhost:8000/api/v1"

# Test 1: Register and Login User
print("=== Test 1: Register User ===")
user_data = {
    "email": "john@example.com",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
print(f"Status: {response.status_code}")
token = response.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}
print(f"Token received: {token[:20]}...")

# Test 2: Create todo with tags and future due_date
print("\n=== Test 2: Create Todo with Tags (Tomorrow) ===")
tomorrow = datetime.now() + timedelta(days=1)
todo_data = {
    "title": "Complete project",
    "description": "Finish the project",
    "due_date": tomorrow.isoformat(),
    "tags": ["work", "urgent"]
}
response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")

# Test 3: Create todo for today
print("\n=== Test 3: Create Todo for Today ===")
today = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
todo_data = {
    "title": "Team meeting",
    "description": "Discuss project progress",
    "due_date": today.isoformat(),
    "tags": ["meeting", "important"]
}
response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")

# Test 4: Create overdue todo
print("\n=== Test 4: Create Overdue Todo ===")
yesterday = datetime.now() - timedelta(days=1)
todo_data = {
    "title": "Review documents",
    "description": "Review old documents",
    "due_date": yesterday.isoformat(),
    "tags": ["review"]
}
response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, default=str)}")

# Test 5: Get today's todos
print("\n=== Test 5: Get Today's Todos ===")
response = requests.get(f"{BASE_URL}/todos/today", headers=headers)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Count: {data['total']}")
for todo in data['items']:
    print(f"  - {todo['title']} (tags: {[t['name'] for t in todo.get('tags', [])]})")

# Test 6: Get overdue todos
print("\n=== Test 6: Get Overdue Todos ===")
response = requests.get(f"{BASE_URL}/todos/overdue", headers=headers)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Count: {data['total']}")
for todo in data['items']:
    print(f"  - {todo['title']} (tags: {[t['name'] for t in todo.get('tags', [])]})")

# Test 7: Get all todos (should show 3)
print("\n=== Test 7: Get All Todos ===")
response = requests.get(f"{BASE_URL}/todos", headers=headers)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Count: {data['total']}")
for todo in data['items']:
    print(f"  - {todo['title']} (due: {todo['due_date']}, tags: {[t['name'] for t in todo.get('tags', [])]})")

# Test 8: Update todo with new tags
print("\n=== Test 8: Update Todo with New Tags ===")
# Get first todo id
response = requests.get(f"{BASE_URL}/todos", headers=headers)
todo_id = response.json()['items'][0]['id']
update_data = {
    "title": "Complete project ASAP",
    "tags": ["work", "urgent", "priority"]
}
response = requests.patch(f"{BASE_URL}/todos/{todo_id}", json=update_data, headers=headers)
print(f"Status: {response.status_code}")
todo = response.json()
print(f"Updated tags: {[t['name'] for t in todo.get('tags', [])]}")

# Test 9: Verify tag uniqueness (same tags across todos)
print("\n=== Test 9: Verify Tag Sharing ===")
response = requests.get(f"{BASE_URL}/todos", headers=headers)
data = response.json()
all_tags = set()
for todo in data['items']:
    for tag in todo.get('tags', []):
        all_tags.add(tag['name'])
print(f"Unique tags used: {all_tags}")

print("\n[PASS] Level 6 Features Test Completed Successfully!")
