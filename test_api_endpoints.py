"""Test the updated API endpoints"""
from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

print("=" * 60)
print("TESTING UPDATED API ENDPOINTS")
print("=" * 60)

# Test /tasks endpoint
print("\n1. Testing /tasks endpoint...")
response = client.get('/tasks')
data = response.json()
print(f"   Status: {response.status_code}")
print(f"   Total tasks: {data.get('total_tasks')}")
print(f"   Validation passed: {data.get('validation', {}).get('validation_passed')}")
print(f"   Tasks: {', '.join([t['name'] for t in data.get('tasks', [])])}")

# Test /validate-tasks endpoint
print("\n2. Testing /validate-tasks endpoint...")
response = client.get('/validate-tasks')
data = response.json()
print(f"   Status: {response.status_code}")
print(f"   Tasks with graders: {data.get('tasks_with_graders')}")
print(f"   Validation passed: {data.get('validation_passed')}")
print(f"   Message: {data.get('message')}")
print(f"   Grader implementations: {', '.join(data.get('grader_implementations', []))}")

print("\n" + "=" * 60)
if data.get('validation_passed'):
    print("✅ ALL API ENDPOINTS WORKING - READY FOR SUBMISSION")
else:
    print("❌ VALIDATION FAILED")
print("=" * 60)
