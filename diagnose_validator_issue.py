#!/usr/bin/env python3
"""
Comprehensive diagnostic to pinpoint where the validator sees fewer tasks
"""
import sys
sys.path.insert(0, '/c/Users/senba/Downloads/Open_env')

print("=" * 70)
print("COMPREHENSIVE DIAGNOSTIC: 5 Tasks with 5 Graders")
print("=" * 70)

# Test 1: Direct imports
print("\n1. TESTING DIRECT IMPORTS:")
try:
    from graders import (
        RewardThresholdGrader, EfficientGrader, RobustnessGrader,
        BatteryEfficientGrader, BalancedMetricsGrader, GRADER_REGISTRY
    )
    print("   ✅ All 5 grader classes imported")
    print(f"   GRADER_REGISTRY has {len(GRADER_REGISTRY)} entries: {list(GRADER_REGISTRY.keys())}")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Tasks registry
print("\n2. TESTING TASKS REGISTRY:")
try:
    from tasks import ALL_TASKS, GRADERS_PER_TASK, validate_tasks, get_task_grader
    print(f"   ✅ ALL_TASKS has {len(ALL_TASKS)} entries:")
    for name in ALL_TASKS.keys():
        print(f"      - {name}")
    print(f"\n   ✅ GRADERS_PER_TASK has {len(GRADERS_PER_TASK)} entries:")
    for name, grader in GRADERS_PER_TASK.items():
        print(f"      - {name}: {grader}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Validate tasks function
print("\n3. TESTING VALIDATE_TASKS():")
try:
    result = validate_tasks()
    print(f"   Total tasks: {result['total_tasks']}")
    print(f"   Tasks with graders: {result['tasks_with_graders']}")
    print(f"   Grader implementations: {result['grader_implementations']}")
    print(f"   Validation passed: {result['validation_passed']}")
    
    print("\n   Task details:")
    for task_name, task_info in result['tasks'].items():
        print(f"      {task_name}: {task_info['grader']} (instantiable: {task_info['instantiable']})")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Instantiate each grader
print("\n4. TESTING GRADER INSTANTIATION:")
try:
    graders_to_test = [
        ("RewardThresholdGrader", RewardThresholdGrader),
        ("EfficientGrader", EfficientGrader),
        ("RobustnessGrader", RobustnessGrader),
        ("BatteryEfficientGrader", BatteryEfficientGrader),
        ("BalancedMetricsGrader", BalancedMetricsGrader),
    ]
    
    for name, grader_class in graders_to_test:
        try:
            # Try to instantiate with default config
            grader = grader_class()
            print(f"   ✅ {name} instantiated")
        except TypeError:
            # Try with empty config
            grader = grader_class(**{})
            print(f"   ✅ {name} instantiated (with empty config)")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Get task grader for each task
print("\n5. TESTING GET_TASK_GRADER():")
try:
    for task_name in ALL_TASKS.keys():
        grader = get_task_grader(task_name)
        print(f"   ✅ {task_name}: {type(grader).__name__}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: openenv.yaml
print("\n6. CHECKING OPENENV.YAML:")
try:
    import yaml
    with open('/c/Users/senba/Downloads/Open_env/openenv.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    tasks_in_yaml = list(config.get('tasks', {}).keys())
    graders_in_yaml = list(config.get('graders', {}).keys())
    
    print(f"   ✅ openenv.yaml has {len(tasks_in_yaml)} tasks: {tasks_in_yaml}")
    print(f"   ✅ openenv.yaml has {len(graders_in_yaml)} graders: {graders_in_yaml}")
    
    # Check if each task has a grader reference
    print("\n   Task-Grader mappings in YAML:")
    for task_name, task_config in config.get('tasks', {}).items():
        grader_info = task_config.get('grader', {})
        grader_class = grader_info.get('class', 'NO CLASS')
        print(f"      {task_name}: {grader_class}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Check __init__.py exports
print("\n7. CHECKING __init__.py EXPORTS:")
try:
    from __init__ import (
        RewardThresholdGrader as Init_RTG,
        EfficientGrader as Init_EG,
        RobustnessGrader as Init_RG,
        BatteryEfficientGrader as Init_BEG,
        BalancedMetricsGrader as Init_BMG,
    )
    print("   ✅ All 5 graders exported from __init__.py")
except ImportError as e:
    print(f"   ❌ Export error: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
