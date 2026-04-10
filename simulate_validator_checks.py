#!/usr/bin/env python3
"""
Test what the external validator might check
"""
import sys
import json

print("=" * 70)
print("VALIDATOR SIMULATION: How the External Validator Checks")
print("=" * 70)

# Simulate what an external validator might do
print("\n1. CHECKING VIA VALIDATE_TASKS() - Local method:")
try:
    from tasks import validate_tasks
    result = validate_tasks()
    
    # External validator might check these fields
    checks = {
        "total_tasks": result.get("total_tasks"),
        "tasks_with_graders": result.get("tasks_with_graders"),
        "validation_passed": result.get("validation_passed"),
        "grader_count": len(result.get("grader_implementations", [])),
    }
    
    for check, value in checks.items():
        print(f"   {check}: {value}")
    
    # What the validator likely checks
    print(f"\n   Validator check:  tasks_with_graders ({checks['tasks_with_graders']}) >= 3?")
    print(f"   Result: {'✅ PASS' if checks['tasks_with_graders'] >= 3 else '❌ FAIL'}")
    
except Exception as e:
    print(f"\n   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Check 2: What about the API endpoint?
print("\n2. CHECKING VIA /validate-tasks endpoint response format:")
try:
    from server.app import app  # This might fail if server isn't properly set up
    print("   ⚠️  Note: Full server simulation would require starting FastAPI app")
    print("   Expected endpoint response should have:")
    print("      - status: 'valid' or 'invalid'")
    print("      - total_tasks: number")
    print("      - tasks_with_graders: number")
    print("      - grader_implementations: list")
    print("      - validation_passed: boolean")
    print("      - message: string")
except Exception as e:
    print(f"   Note: {e.__class__.__name__} - This is expected if server not running")

# Check 3: Manual verification
print("\n3. MANUAL VERIFICATION OF REQUIREMENTS:")
try:
    from tasks import ALL_TASKS, GRADERS_PER_TASK
    from graders import GRADER_REGISTRY
    
    # Requirement 1: At least 3 tasks
    print(f"   Requirement 1: At least 3 tasks")
    print(f"      ALL_TASKS count: {len(ALL_TASKS)}")
    print(f"      Status: {'✅ PASS' if len(ALL_TASKS) >= 3 else '❌ FAIL'}")
    
    # Requirement 2: Each task has a grader
    print(f"\n   Requirement 2: Each task has a grader")
    all_have_graders = all(task_name in GRADERS_PER_TASK for task_name in ALL_TASKS.keys())
    print(f"      All {len(ALL_TASKS)} tasks have graders: {'✅ YES' if all_have_graders else '❌ NO'}")
    
    # Requirement 3: Graders are instantiable
    print(f"\n   Requirement 3: Graders are instantiable")
    try:
        from tasks import get_task_grader
        for task_name in ALL_TASKS.keys():
            grader = get_task_grader(task_name)
            print(f"      {task_name}: ✅ {type(grader).__name__}")
    except Exception as grader_err:
        print(f"      ❌ Error: {grader_err}")
    
    # Requirement 4: Graders work
    print(f"\n   Requirement 4: Graders return valid scores")
    try:
        from server.environment import MeshNetworkEnvironment
        from models import TaskDifficulty, MeshAction
        
        # Test with easy task/grader
        grader = get_task_grader("easy")
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        obs = env.reset(seed=42)
        
        def dummy_agent(obs):
            if obs.neighboring_devices:
                return MeshAction(target_device_id=obs.neighboring_devices[0].device_id)
            return MeshAction(target_device_id=obs.current_device_id)
        
        # Try to grade
        try:
            # Need to check what method graders have
            if hasattr(grader, 'grade_task'):
                score = grader.grade_task(dummy_agent, TaskDifficulty.EASY)
            else:
                # Try something else
                score = None
            
            if score is not None:
                print(f"      Sample score (easy): {score}")
                print(f"      Score is (0, 1)? {0 < score < 1} {'✅' if 0 < score < 1 else '❌'}")
            else:
                print(f"      ⚠️  Could not evaluate score format")
        except Exception as scoring_err:
            print(f"      Note: Scoring test not fully runnable in this context: {scoring_err}")
            
    except Exception as env_err:
        print(f"      Note: Environment test skipped: {env_err}")

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
print("If all checks above show ✅, then the code passes requirements locally.")
print("If external validator still fails, possible causes:")
print("  1. HF Spaces hasn't redeployed (clear cache/restart)")
print("  2. Validator checks a different endpoint or format")
print("  3. Validator running old code from different branch")
print("=" * 70)
