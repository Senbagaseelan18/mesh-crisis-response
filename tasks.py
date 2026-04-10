"""
Task definitions with grainer assignments for OpenEnv Phase 2+
Explicit task registry for validator discovery
5 TASKS with 5 DIFFERENT GRADERS - ENHANCED COVERAGE
"""

from dataclasses import dataclass
from typing import Dict, Any, Type
from models import TaskDifficulty
from graders import BaseGrader, RewardThresholdGrader, EfficientGrader, RobustnessGrader, BatteryEfficientGrader, BalancedMetricsGrader


@dataclass
class Task:
    """Represents a task with its grader configuration"""
    name: str
    difficulty: TaskDifficulty
    description: str
    max_steps: int
    grader_class: Type[BaseGrader]
    grader_config: Dict[str, Any]


# TASK 1: Easy - Direct Path
EASY_TASK = Task(
    name="easy",
    difficulty=TaskDifficulty.EASY,
    description="Gateway is 1 hop away, high battery",
    max_steps=5,
    grader_class=RewardThresholdGrader,
    grader_config={
        "min_reward": 0.0,
        "max_reward": 1.0,
        "success_threshold": 0.8
    }
)

# TASK 2: Medium - Multi-hop
MEDIUM_TASK = Task(
    name="medium",
    difficulty=TaskDifficulty.MEDIUM,
    description="Gateway is 3 hops away, moderate battery",
    max_steps=10,
    grader_class=EfficientGrader,
    grader_config={
        "success_threshold": 0.6
    }
)

# TASK 3: Hard - Long Distance
HARD_TASK = Task(
    name="hard",
    difficulty=TaskDifficulty.HARD,
    description="Gateway is 5+ hops away, low battery",
    max_steps=20,
    grader_class=RobustnessGrader,
    grader_config={
        "success_threshold": 0.5
    }
)

# TASK 4: Expert - Battery Constrained
EXPERT_TASK = Task(
    name="expert",
    difficulty=TaskDifficulty.HARD,
    description="Gateway is far away with severe battery constraints",
    max_steps=25,
    grader_class=BatteryEfficientGrader,
    grader_config={
        "success_threshold": 0.55
    }
)

# TASK 5: Extreme - Balanced Performance
EXTREME_TASK = Task(
    name="extreme",
    difficulty=TaskDifficulty.HARD,
    description="Extreme challenge requiring balanced performance across all metrics",
    max_steps=30,
    grader_class=BalancedMetricsGrader,
    grader_config={
        "success_threshold": 0.5
    }
)

# REGISTRY: All tasks in a discoverable format
ALL_TASKS = {
    "easy": EASY_TASK,
    "medium": MEDIUM_TASK,
    "hard": HARD_TASK,
    "expert": EXPERT_TASK,
    "extreme": EXTREME_TASK,
}

# Count graders
AVAILABLE_TASKS_COUNT = len(ALL_TASKS)
GRADERS_PER_TASK = {
    "easy": "RewardThresholdGrader",
    "medium": "EfficientGrader",
    "hard": "RobustnessGrader",
    "expert": "BatteryEfficientGrader",
    "extreme": "BalancedMetricsGrader",
}


def get_all_tasks() -> Dict[str, Task]:
    """Get all available tasks with graders"""
    return ALL_TASKS


def get_task(task_name: str) -> Task:
    """Get a specific task by name"""
    if task_name not in ALL_TASKS:
        raise ValueError(f"Unknown task: {task_name}. Available: {list(ALL_TASKS.keys())}")
    return ALL_TASKS[task_name]


def get_task_grader(task_name: str) -> BaseGrader:
    """Instantiate the grader for a specific task"""
    task = get_task(task_name)
    return task.grader_class(**task.grader_config)


def validate_tasks() -> Dict[str, Any]:
    """Validate that all tasks have proper grader assignments"""
    validation_result = {
        "total_tasks": len(ALL_TASKS),
        "tasks_with_graders": 0,
        "grader_implementations": [],
        "tasks": {}
    }
    
    for task_name, task in ALL_TASKS.items():
        grader_instance = get_task_grader(task_name)
        validation_result["tasks"][task_name] = {
            "difficulty": task.difficulty.value,
            "grader": task.grader_class.__name__,
            "grader_type": GRADERS_PER_TASK[task_name],
            "instantiable": True
        }
        validation_result["tasks_with_graders"] += 1
        
        grader_name = task.grader_class.__name__
        if grader_name not in validation_result["grader_implementations"]:
            validation_result["grader_implementations"].append(grader_name)
    
    validation_result["validation_passed"] = validation_result["tasks_with_graders"] >= 3
    return validation_result


if __name__ == "__main__":
    # Test the tasks registry
    print("=" * 60)
    print("TASKS REGISTRY VALIDATION - 5 TASKS WITH 5 GRADERS")
    print("=" * 60)
    
    result = validate_tasks()
    print(f"\nTotal Tasks: {result['total_tasks']}")
    print(f"Tasks with Graders: {result['tasks_with_graders']}")
    print(f"Grader Implementations: {', '.join(result['grader_implementations'])}")
    
    print("\nTask Details:")
    for task_name, task_info in result["tasks"].items():
        print(f"\n  {task_name.upper()}:")
        print(f"    Difficulty: {task_info['difficulty']}")
        print(f"    Grader: {task_info['grader']}")
        print(f"    Type: {task_info['grader_type']}")
        print(f"    Instantiable: {task_info['instantiable']}")
    
    print("\n" + "=" * 60)
    if result["validation_passed"]:
        print("✅ VALIDATION PASSED: 3+ tasks with graders")
    else:
        print("❌ VALIDATION FAILED: Less than 3 tasks with graders")
    print("=" * 60)
