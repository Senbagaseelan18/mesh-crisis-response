"""Emergency Mesh-Network Router Package"""
__version__ = "1.0.0"

# Export models
from models import (
    MeshObservation,
    MeshAction,
    MeshState,
    DeviceNode,
    TaskDifficulty,
    RewardInfo,
    TaskGradeResult,
)

# Export graders
from graders import (
    BaseGrader,
    RewardThresholdGrader,
    EfficientGrader,
    RobustnessGrader,
    get_grader,
    GRADER_REGISTRY,
)

# Export tasks registry - CRITICAL FOR VALIDATOR DISCOVERY
from tasks import (
    Task,
    ALL_TASKS,
    EASY_TASK,
    MEDIUM_TASK,
    HARD_TASK,
    get_all_tasks,
    get_task,
    get_task_grader,
    validate_tasks,
    AVAILABLE_TASKS_COUNT,
    GRADERS_PER_TASK,
)

# Export environment
from server.environment import MeshNetworkEnvironment, TaskGrader

__all__ = [
    # Models
    "MeshObservation",
    "MeshAction",
    "MeshState",
    "DeviceNode",
    "TaskDifficulty",
    "RewardInfo",
    "TaskGradeResult",
    # Graders
    "BaseGrader",
    "RewardThresholdGrader",
    "EfficientGrader",
    "RobustnessGrader",
    "get_grader",
    "GRADER_REGISTRY",
    # Tasks - CRITICAL FOR VALIDATOR
    "Task",
    "ALL_TASKS",
    "EASY_TASK",
    "MEDIUM_TASK", 
    "HARD_TASK",
    "get_all_tasks",
    "get_task",
    "get_task_grader",
    "validate_tasks",
    "AVAILABLE_TASKS_COUNT",
    "GRADERS_PER_TASK",
    # Environment
    "MeshNetworkEnvironment",
    "TaskGrader",
]
