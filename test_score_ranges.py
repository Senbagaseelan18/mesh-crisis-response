"""Test grader score ranges for validator compliance"""
from tasks import get_task_grader
from server.environment import MeshNetworkEnvironment
from models import MeshObservation, MeshAction, TaskDifficulty

print("=" * 60)
print("TESTING GRADER SCORE RANGES")
print("=" * 60)

def simple_agent(obs: MeshObservation) -> MeshAction:
    """Simple agent for testing"""
    if obs.neighboring_devices:
        target = obs.neighboring_devices[0]
        return MeshAction(target_device_id=target.device_id, priority=1)
    return MeshAction(target_device_id="node_0", priority=1)

tasks_to_test = ["easy", "medium", "hard"]

for task_name in tasks_to_test:
    print(f"\nTesting {task_name.upper()}:")
    print("-" * 60)
    
    grader = get_task_grader(task_name)
    env = MeshNetworkEnvironment(task_difficulty=TaskDifficulty[task_name.upper()])
    
    result = grader.grade(simple_agent, env, n_episodes=3)
    score = result.get("score")
    
    print(f"  Grader: {grader.__class__.__name__}")
    print(f"  Score: {score}")
    print(f"  Type: {type(score)}")
    print(f"  In range (0, 1)? {0 < score < 1}")
    
    if score <= 0.0 or score >= 1.0:
        print(f"  ⚠️  WARNING: Score {score} is on boundary!")
    else:
        print(f"  ✅ Score is valid (strictly between 0 and 1)")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)
