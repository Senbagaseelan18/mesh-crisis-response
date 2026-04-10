"""Test script to validate graders configuration"""
from graders import RewardThresholdGrader, EfficientGrader, RobustnessGrader
import yaml

print('✅ All graders imported successfully')

# Test instantiation
r_grader = RewardThresholdGrader(min_reward=0.0, max_reward=1.0, success_threshold=0.8)
e_grader = EfficientGrader(success_threshold=0.6)
rob_grader = RobustnessGrader(success_threshold=0.5)

print('✅ All graders instantiated successfully')

# Validate openenv.yaml
with open('openenv.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
tasks = config.get('tasks', {})
print(f'✅ Found {len(tasks)} tasks: {list(tasks.keys())}')

task_count_with_graders = 0
for task_name, task_config in tasks.items():
    if 'grader' in task_config:
        grader_class = task_config['grader'].get('class', 'N/A')
        print(f'  ✅ Task "{task_name}" has grader: {grader_class}')
        task_count_with_graders += 1
    else:
        print(f'  ❌ Task "{task_name}" missing grader!')

graders = config.get('graders', {})
print(f'✅ Found {len(graders)} grader definitions: {list(graders.keys())}')

print(f'\n📊 Summary:')
print(f'   Total tasks: {len(tasks)}')
print(f'   Tasks with graders: {task_count_with_graders}')
print(f'   Grader implementations: {len(graders)}')

if task_count_with_graders >= 3:
    print(f'\n✅ VALIDATION PASSED: {task_count_with_graders} tasks with graders (need ≥3)')
else:
    print(f'\n❌ VALIDATION FAILED: Only {task_count_with_graders} tasks with graders (need ≥3)')
