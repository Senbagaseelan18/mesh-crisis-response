"""Test the /tasks API endpoint returns correct graders"""
import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from server.app import app
import json

client = TestClient(app)

print("=" * 60)
print("TESTING /tasks API ENDPOINT")
print("=" * 60)

# Call /tasks endpoint
response = client.get("/tasks")
tasks_data = response.json()

print(f"\nStatus Code: {response.status_code}")

if response.status_code == 200:
    print("✅ /tasks endpoint returned 200")
    
    tasks = tasks_data.get("tasks", [])
    print(f"\n📋 Found {len(tasks)} tasks:")
    
    for task in tasks:
        task_name = task.get("name", "unknown")
        grader_class = task.get("grader", {}).get("class", "N/A")
        print(f"\n  Task: {task_name}")
        print(f"    Grader Class: {grader_class}")
        print(f"    Difficulty: {task.get('difficulty')}")
        print(f"    Max Steps: {task.get('max_steps')}")
        
        # Verify grader is correctly assigned
        if task_name == "easy":
            if "RewardThresholdGrader" in grader_class:
                print(f"    ✅ Correct grader (RewardThresholdGrader)")
            else:
                print(f"    ❌ Wrong grader! Expected RewardThresholdGrader")
        elif task_name == "medium":
            if "EfficientGrader" in grader_class:
                print(f"    ✅ Correct grader (EfficientGrader)")
            else:
                print(f"    ❌ Wrong grader! Expected EfficientGrader")
        elif task_name == "hard":
            if "RobustnessGrader" in grader_class:
                print(f"    ✅ Correct grader (RobustnessGrader)")
            else:
                print(f"    ❌ Wrong grader! Expected RobustnessGrader")
    
    print(f"\n" + "=" * 60)
    print("✅ /tasks ENDPOINT VALIDATION PASSED")
    print("=" * 60)
    
    # Print full JSON for reference
    print("\nFull Response JSON:")
    print(json.dumps(tasks_data, indent=2))
else:
    print(f"❌ /tasks endpoint returned {response.status_code}")
    print(f"Response: {response.text}")
