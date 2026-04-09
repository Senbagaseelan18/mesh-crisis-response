#!/usr/bin/env python3
"""
Test script to verify all grader endpoints are working
Run this after HF Space rebuilds to confirm Phase 2 compliance
"""

import requests
import json
import sys
from typing import Optional

# Configuration
BASE_URL = "https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router"
# For local testing:
# BASE_URL = "http://localhost:8000"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text: str):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")

def print_success(text: str):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text: str):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text: str):
    print(f"{YELLOW}⚠ {text}{RESET}")

def test_endpoint(method: str, endpoint: str, data: Optional[dict] = None) -> bool:
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return False
        
        if response.status_code in [200, 201]:
            return True, response.json()
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
    
    except Exception as e:
        return False, str(e)

def main():
    print(f"\n{BOLD}Emergency Mesh Router - Phase 2 Grader Verification{RESET}")
    print(f"Testing: {BASE_URL}\n")
    
    all_passed = True
    
    # =========================================================================
    # Test 1: Health Check
    # =========================================================================
    print_header("1. Health Check")
    success, result = test_endpoint("GET", "/health")
    if success:
        print_success(f"Health endpoint working: {result}")
    else:
        print_error(f"Health endpoint failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 2: Tasks Endpoint
    # =========================================================================
    print_header("2. Tasks Endpoint (/tasks)")
    success, result = test_endpoint("GET", "/tasks")
    if success:
        tasks = result.get("tasks", [])
        print_success(f"Tasks endpoint working. Found {len(tasks)} tasks:")
        for task in tasks:
            print(f"   - {task.get('name')} (difficulty {task.get('difficulty')})")
            if task.get('grader'):
                print(f"     Grader: {task.get('grader')} ✓")
            else:
                print_warning(f"     Grader not specified!")
        
        if len(tasks) < 3:
            print_error(f"ERROR: Need at least 3 tasks, found {len(tasks)}")
            all_passed = False
    else:
        print_error(f"Tasks endpoint failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 3: Graders Endpoint
    # =========================================================================
    print_header("3. Graders Endpoint (/graders)")
    success, result = test_endpoint("GET", "/graders")
    if success:
        graders = result.get("graders", [])
        print_success(f"Graders endpoint working. Found {len(graders)} graders:")
        for grader in graders:
            print(f"   - {grader.get('name')} ({grader.get('type')})")
            tasks_supported = grader.get('supported_tasks', [])
            print(f"     Supports tasks: {', '.join(tasks_supported)}")
    else:
        print_error(f"Graders endpoint failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 4: Grade Easy Task
    # =========================================================================
    print_header("4. Grade Easy Task (/grade/easy)")
    success, result = test_endpoint("GET", "/grade/easy?n_episodes=3")
    if success:
        print_success(f"Easy grader working:")
        print(f"   Score: {result.get('score'):.3f}")
        print(f"   Success Rate: {result.get('success_rate'):.1%}")
        print(f"   Avg Hops: {result.get('average_hops'):.1f}")
        print(f"   Avg Reward: {result.get('average_reward'):.2f}")
        
        score = result.get('score', 0)
        if 0.0 <= score <= 1.0:
            print_success(f"Score in valid range [0.0, 1.0]")
        else:
            print_error(f"Score {score} out of valid range!")
            all_passed = False
    else:
        print_error(f"Easy grader failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 5: Grade Medium Task
    # =========================================================================
    print_header("5. Grade Medium Task (/grade/medium)")
    success, result = test_endpoint("GET", "/grade/medium?n_episodes=3")
    if success:
        print_success(f"Medium grader working:")
        print(f"   Score: {result.get('score'):.3f}")
        print(f"   Success Rate: {result.get('success_rate'):.1%}")
        print(f"   Avg Hops: {result.get('average_hops'):.1f}")
        print(f"   Avg Reward: {result.get('average_reward'):.2f}")
        
        score = result.get('score', 0)
        if 0.0 <= score <= 1.0:
            print_success(f"Score in valid range [0.0, 1.0]")
        else:
            print_error(f"Score {score} out of valid range!")
            all_passed = False
    else:
        print_error(f"Medium grader failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 6: Grade Hard Task
    # =========================================================================
    print_header("6. Grade Hard Task (/grade/hard)")
    success, result = test_endpoint("GET", "/grade/hard?n_episodes=3")
    if success:
        print_success(f"Hard grader working:")
        print(f"   Score: {result.get('score'):.3f}")
        print(f"   Success Rate: {result.get('success_rate'):.1%}")
        print(f"   Avg Hops: {result.get('average_hops'):.1f}")
        print(f"   Avg Reward: {result.get('average_reward'):.2f}")
        
        score = result.get('score', 0)
        if 0.0 <= score <= 1.0:
            print_success(f"Score in valid range [0.0, 1.0]")
        else:
            print_error(f"Score {score} out of valid range!")
            all_passed = False
    else:
        print_error(f"Hard grader failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 7: POST /grade Endpoint
    # =========================================================================
    print_header("7. POST /grade Endpoint")
    success, result = test_endpoint("POST", "/grade", {"difficulty": "easy", "n_episodes": 3})
    if success:
        print_success(f"POST /grade working:")
        print(f"   Score: {result.get('score'):.3f}")
        print(f"   Success Rate: {result.get('success_rate'):.1%}")
    else:
        print_error(f"POST /grade failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Test 8: Validation Endpoint
    # =========================================================================
    print_header("8. Validation Endpoint (/validate)")
    success, result = test_endpoint("GET", "/validate")
    if success:
        print_success(f"Validation endpoint working")
        
        # Check structure
        required_keys = ["openenv_spec", "endpoints", "tasks_with_graders", "models"]
        for key in required_keys:
            if key in result:
                print_success(f"   {key}: present")
            else:
                print_error(f"   {key}: MISSING")
                all_passed = False
        
        # Check all tasks have graders
        tasks_graders = result.get("tasks_with_graders", {})
        for task_name in ["easy", "medium", "hard"]:
            if task_name in tasks_graders and tasks_graders[task_name]:
                print_success(f"   Task '{task_name}' has grader")
            else:
                print_error(f"   Task '{task_name}' MISSING GRADER")
                all_passed = False
    else:
        print_error(f"Validation endpoint failed: {result}")
        all_passed = False
    
    # =========================================================================
    # Final Summary
    # =========================================================================
    print_header("SUMMARY")
    
    if all_passed:
        print_success("All grader endpoints working correctly!")
        print_success("Phase 2 compliance check: PASSED ✓")
        print(f"\n{BOLD}{GREEN}Ready to resubmit!{RESET}\n")
        return 0
    else:
        print_error("Some tests failed. Check output above.")
        print_error("Phase 2 compliance check: FAILED")
        print(f"\n{BOLD}{RED}Do not resubmit yet.{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
