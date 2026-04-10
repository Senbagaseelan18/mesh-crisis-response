#!/usr/bin/env python3
"""
Final test: Show EXACTLY what the phase 2 validator should see
This mimics what the HF Spaces / hackathon validator likely checks
"""

import json

print("=" * 80)
print("PHASE 2 VALIDATOR CHECK - EXACT SIMULATION")
print("=" * 80)

print("\n[VALIDATOR] Checking for minimum 3 tasks with graders...")
print("-" * 80)

# Step 1: Import and validate
print("\n[VALIDATOR STEP 1] Importing tasks and validating...")
try:
    from tasks import validate_tasks, get_all_tasks, get_task_grader
    result = validate_tasks()
    
    print(f"  ✅ Tasks module imported")
    print(f"  ✅ Validation function executed")
    print(f"\n  Validation result:")
    print(f"    - Total tasks found: {result['total_tasks']}")
    print(f"    - Tasks with graders: {result['tasks_with_graders']}")
    print(f"    - Different grader types: {len(result['grader_implementations'])}")
    print(f"    - Validation status: {'PASS' if result['validation_passed'] else 'FAIL'}")
    
    # This is what the validator checks
    validator_check = result['tasks_with_graders'] >= 3
    print(f"\n  [CRITICAL CHECK] tasks_with_graders ({result['tasks_with_graders']}) >= 3 ?")
    print(f"  Result: {'✅ YES - WOULD PASS' if validator_check else '❌ NO - WOULD FAIL'}")
    
    if not validator_check:
        print(f"\n  🚨 ERROR: Only {result['tasks_with_graders']} tasks with graders found!")
        print(f"     Message: Not enough tasks with graders")
    else:
        print(f"\n  ✅ SUCCESS: {result['tasks_with_graders']} tasks with graders found!")
    
except Exception as e:
    print(f"  ❌ ERROR during validation: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 2: Verify each task individually
print("\n" + "-" * 80)
print("\n[VALIDATOR STEP 2] Verifying each task has a working grader...")

try:
    all_tasks = get_all_tasks()
    all_good = True
    
    for task_name in all_tasks.keys():
        try:
            grader = get_task_grader(task_name)
            print(f"  ✅ {task_name}: {type(grader).__name__}")
        except Exception as e:
            print(f"  ❌ {task_name}: {e}")
            all_good = False
    
    if all_good:
        print(f"\n  ✅ All tasks have working graders")
    else:
        print(f"\n  ❌ Some tasks have issues")
        
except Exception as e:
    print(f"  ❌ ERROR checking tasks: {e}")

# Step 3: Show endpoint response format
print("\n" + "-" * 80)
print("\n[VALIDATOR STEP 3] /validate-tasks endpoint response (if called)...")

try:
    # If the validator calls /validate-tasks endpoint, this is what it gets
    endpoint_response = {
        "status": "valid" if result["validation_passed"] else "invalid",
        "total_tasks": result["total_tasks"],
        "tasks_with_graders": result["tasks_with_graders"],
        "grader_implementations": result["grader_implementations"],
        "task_details": result["tasks"],
        "validation_passed": result["validation_passed"],
        "message": f"✅ Submission has {result['tasks_with_graders']} tasks with graders" if result["validation_passed"] else "❌ Not enough tasks with graders"
    }
    
    print(f"\n  Expected response format:")
    print(f"  ```json")
    print(json.dumps(endpoint_response, indent=2))
    print(f"  ```")
    
except Exception as e:
    print(f"  ❌ ERROR: {e}")

# Step 4: Show openenv.yaml check
print("\n" + "-" * 80)
print("\n[VALIDATOR STEP 4] Checking openenv.yaml task/grader definitions...")

try:
    import yaml
    with open('openenv.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    yaml_tasks = config.get('tasks', {})
    yaml_graders = config.get('graders', {})
    
    print(f"\n  Tasks in openenv.yaml: {len(yaml_tasks)}")
    for task_name in yaml_tasks.keys():
        grader_ref = yaml_tasks[task_name].get('grader', {}).get('class', 'UNKNOWN')
        print(f"    - {task_name}: {grader_ref}")
    
    print(f"\n  Graders in openenv.yaml: {len(yaml_graders)}")
    for grader_name in yaml_graders.keys():
        grader_class = yaml_graders[grader_name].get('class', 'UNKNOWN')
        print(f"    - {grader_name}: {grader_class}")
    
    yaml_check = len(yaml_tasks) >= 3
    print(f"\n  [CHECK] Tasks in YAML ({len(yaml_tasks)}) >= 3 ?")
    print(f"  Result: {'✅ YES' if yaml_check else '❌ NO'}")
    
except Exception as e:
    print(f"  ⚠️  Could not check openenv.yaml: {e}")

# Final summary
print("\n" + "=" * 80)
print("FINAL VERDICT:")
print("=" * 80)

try:
    result = validate_tasks()
    
    checks = {
        "Python validation function": result['validation_passed'],
        "Tasks count >= 3": result['tasks_with_graders'] >= 3,
        "All graders instantiable": len(result['grader_implementations']) == result['tasks_with_graders'],
    }
    
    all_pass = all(checks.values())
    
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {check_name}")
    
    print(f"\n  Overall: {'✅ SHOULD PASS' if all_pass else '❌ SHOULD FAIL'}")
    
    if all_pass:
        print(f"\n  📊 Code Status: READY FOR SUBMISSION")
        print(f"     - Valid implementation with {result['tasks_with_graders']} tasks")
        print(f"     - Different grader types: {result['grader_implementations']}")
    else:
        print(f"\n  🚨 There are issues to fix before submission")
        
except Exception as e:
    print(f"  ❌ ERROR: {e}")

print("\n" + "=" * 80)
