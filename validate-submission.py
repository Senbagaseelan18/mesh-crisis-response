#!/usr/bin/env python3
"""
Validation script for OpenEnv hackathon submission.
Checks that all required endpoints work and return correct format.

Usage:
    python validate-submission.py http://localhost:8000
    python validate-submission.py https://huggingface.co/spaces/username/env-name
"""

import sys
import requests
import json
import argparse
from typing import Tuple

def check_endpoint(url: str, method: str = "GET", data: dict = None) -> Tuple[bool, str]:
    """Check if endpoint is accessible."""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            return True, response.text[:100]
        else:
            return False, f"Status {response.status_code}"
    except Exception as e:
        return False, str(e)

def validate_submission(base_url: str) -> bool:
    """Validate all required endpoints for hackathon submission."""
    
    # Normalize URL
    base_url = base_url.rstrip('/')
    
    print(f"\n🧪 VALIDATING OPENENV HACKATHON SUBMISSION")
    print(f"📍 URL: {base_url}")
    print("=" * 60)
    
    endpoints = [
        # Health checks
        ("/health", "GET", None, "Health Check"),
        ("/", "GET", None, "Root Endpoint"),
        ("/tasks", "GET", None, "Tasks List"),
        ("/docs", "GET", None, "Documentation"),
        
        # Environment endpoints (with difficulty)
        ("/reset/easy", "POST", {}, "Reset Easy"),
        ("/reset/medium", "POST", {}, "Reset Medium"),
        ("/reset/hard", "POST", {}, "Reset Hard"),
        
        # State endpoints
        ("/state/easy", "GET", None, "Get State Easy"),
        ("/episode-stats/easy", "GET", None, "Episode Stats Easy"),
        
        # Grade endpoint
        ("/grade/easy?n_episodes=1", "POST", {}, "Grade Easy (1 episode)"),
    ]
    
    passed = 0
    failed = 0
    
    for endpoint, method, data, description in endpoints:
        full_url = f"{base_url}{endpoint}"
        success, response = check_endpoint(full_url, method, data)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {description:30} | {endpoint}")
        
        if success:
            passed += 1
        else:
            failed += 1
            print(f"       Response: {response}")
    
    print("=" * 60)
    print(f"\n📊 RESULTS")
    print(f"   Passed: {passed}/{len(endpoints)}")
    print(f"   Failed: {failed}/{len(endpoints)}")
    
    if failed == 0:
        print(f"\n✅ ALL CHECKS PASSED - Ready for submission!")
        return True
    else:
        print(f"\n❌ {failed} CHECK(S) FAILED - Fix issues before submitting")
        return False

def validate_inference() -> bool:
    """Validate that inference.py exists and runs."""
    print("\n" + "=" * 60)
    print("🤖 VALIDATING INFERENCE SCRIPT")
    print("=" * 60)
    
    try:
        import subprocess
        # Try importing inference module
        from inference import run_inference
        
        print("✅ inference.py exists and is importable")
        
        # Try run_inference function
        results = run_inference(task="easy", agent_name="random", n_episodes=1, verbose=False)
        
        if results and "score" in results:
            print("✅ inference.run_inference() works correctly")
            print(f"   Sample result score: {results['score']:.2f}")
            return True
        else:
            print("❌ inference.run_inference() returned invalid result")
            return False
            
    except ImportError as e:
        print(f"❌ Cannot import inference: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running inference: {e}")
        return False

def validate_models() -> bool:
    """Validate that required models are defined."""
    print("\n" + "=" * 60)
    print("📦 VALIDATING MODELS")
    print("=" * 60)
    
    required_classes = [
        "TaskDifficulty", "DeviceNode", "MeshObservation", 
        "MeshAction", "MeshState", "RewardInfo", "TaskGradeResult"
    ]
    
    try:
        from models import (
            TaskDifficulty, DeviceNode, MeshObservation,
            MeshAction, MeshState, RewardInfo, TaskGradeResult
        )
        
        for cls_name in required_classes:
            print(f"✅ {cls_name}")
        
        return True
    except ImportError as e:
        print(f"❌ Missing model class: {e}")
        return False

def validate_environment() -> bool:
    """Validate that environment works locally."""
    print("\n" + "=" * 60)
    print("🌍 VALIDATING ENVIRONMENT")
    print("=" * 60)
    
    try:
        from server.environment import MeshNetworkEnvironment, TaskGrader
        from models import TaskDifficulty, MeshAction
        
        # Test EASY
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        obs = env.reset(seed=42)
        print("✅ Easy environment initializes")
        
        # Take a step
        if obs.neighboring_devices:
            action = MeshAction(target_device_id=obs.neighboring_devices[0].device_id)
            obs, reward, done, info = env.step(action)
            print("✅ Easy environment step works")
        
        # Test MEDIUM
        env = MeshNetworkEnvironment(TaskDifficulty.MEDIUM)
        obs = env.reset(seed=42)
        print("✅ Medium environment initializes")
        
        # Test HARD
        env = MeshNetworkEnvironment(TaskDifficulty.HARD)
        obs = env.reset(seed=42)
        print("✅ Hard environment initializes")
        
        # Test grader
        grader = TaskGrader(n_episodes=1)
        def dummy_agent(obs):
            return MeshAction(target_device_id=obs.current_device_id)
        
        result = grader.grade_task(dummy_agent, TaskDifficulty.EASY)
        print("✅ TaskGrader works")
        
        return True
    except Exception as e:
        print(f"❌ Environment error: {e}")
        return False

def main():
    """Main validation entry point."""
    parser = argparse.ArgumentParser(description="Validate OpenEnv hackathon submission")
    parser.add_argument("url", nargs="?", default="http://localhost:8000",
                       help="Base URL of the environment API (default: http://localhost:8000)")
    parser.add_argument("--local-only", action="store_true",
                       help="Only validate local components (no URL check)")
    
    args = parser.parse_args()
    
    results = []
    
    # Validate local components
    print("\n🔍 LOCAL VALIDATION")
    results.append(("Models", validate_models()))
    results.append(("Environment", validate_environment()))
    results.append(("Inference", validate_inference()))
    
    # Validate API endpoints
    if not args.local_only:
        print("\n🌐 API ENDPOINT VALIDATION")
        results.append(("API Endpoints", validate_submission(args.url)))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 READY FOR SUBMISSION!")
        return 0
    else:
        print(f"\n⚠️  Fix {total - passed} remaining issue(s)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
