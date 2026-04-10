#!/usr/bin/env python3
"""
Test what the /tasks endpoint returns - this is what the validator checks
"""
import json
from tasks import get_all_tasks, validate_tasks

print("=" * 80)
print("CHECKING /tasks ENDPOINT RESPONSE")
print("=" * 80)

all_tasks = get_all_tasks()
tasks_response = []

for task_name, task in all_tasks.items():
    tasks_response.append({
        "name": task.name,
       "difficulty": task.difficulty.value,
        "description": task.description,
        "max_steps": task.max_steps,
        "grader": {
            "class": f"graders.{task.grader_class.__name__}",
            "module": "graders",
            "type": task.grader_class.__name__,
            "config": task.grader_config
        }
    })

endpoint_response = {
    "tasks": tasks_response,
    "total_tasks": len(tasks_response),
    "validation": validate_tasks()
}

print("\nEndpoint Response (/tasks):")
print(json.dumps(endpoint_response, indent=2, default=str))

print("\n" + "=" * 80)
print("ANALYSIS:")
print("=" * 80)

# Count tasks with graders in response
tasks_with_graders = 0
for task in tasks_response:
    if "grader" in task and task["grader"] and task["grader"].get("class"):
        tasks_with_graders += 1
        print(f"✅ {task['name']:40} has grader: {task['grader']['type']}")

print(f"\n✅ Total tasks: {len(tasks_response)}")
print(f"✅ Tasks with graders: {tasks_with_graders}")
print(f"✅ Validation passed: {endpoint_response['validation']['validation_passed']}")

print("\n" + "=" * 80)
print("CONCLUSION:")
print("=" * 80)
if tasks_with_graders >= 3:
    print(f"✅ PASS: {tasks_with_graders} tasks with graders (requirement: >= 3)")
else:
    print(f"❌ FAIL: {tasks_with_graders} tasks with graders (requirement: >= 3)")

print("=" * 80)
