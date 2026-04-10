#!/usr/bin/env python3
"""
Quick validation test for OpenEnv environment endpoints.
Run this locally to verify all required endpoints are working.
"""

import requests
import json
import time
import subprocess
import sys
import os

def test_endpoints(base_url="http://localhost:8000", timeout=5):
    """Test all required OpenEnv endpoints."""
    
    endpoints = {
        "GET /": ("GET", "/"),
        "GET /health": ("GET", "/health"),
        "GET /tasks": ("GET", "/tasks"),
        "GET /docs": ("GET", "/docs"),
        "POST /reset": ("POST", "/reset"),
        "POST /reset/easy": ("POST", "/reset/easy"),
        "POST /reset/medium": ("POST", "/reset/medium"),
        "POST /reset/hard": ("POST", "/reset/hard"),
        "GET /state/easy": ("GET", "/state/easy"),
        "GET /episode-stats/easy": ("GET", "/episode-stats/easy"),
        "POST /grade/easy": ("POST", "/grade/easy"),
        "GET /api/network-topology/easy": ("GET", "/api/network-topology/easy"),
        "GET /api/run-episode/easy/greedy": ("GET", "/api/run-episode/easy/greedy"),
    }
    
    print("\n🧪 TESTING OPENENV ENDPOINTS")
    print("=" * 70)
    print(f"🌐 Server: {base_url}")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for name, (method, path) in endpoints.items():
        url = base_url + path
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            else:  # POST
                response = requests.post(url, json={}, timeout=timeout)
            
            if response.status_code in [200, 201, 202]:
                status = "✅ PASS"
                passed += 1
            else:
                status = f"⚠️  ({response.status_code})"
                failed += 1
            
            # Show first 50 chars of response
            try:
                data = response.json()
                resp_summary = json.dumps(data)[:50]
            except:
                resp_summary = response.text[:50]
            
            print(f"{status} | {name:30} | {resp_summary}")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ FAIL | {name:30} | Connection refused")
            failed += 1
        except Exception as e:
            print(f"❌ FAIL | {name:30} | {str(e)[:50]}")
            failed += 1
    
    print("=" * 70)
    print(f"\n📊 RESULTS: {passed} passed, {failed} failed out of {len(endpoints)} tests")
    
    if failed == 0:
        print("✅ ALL ENDPOINTS WORKING!\n")
        return True
    else:
        print(f"❌ {failed} ENDPOINT(S) FAILED\n")
        return False

if __name__ == "__main__":
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    # Test the endpoints
    success = test_endpoints(base_url)
    
    sys.exit(0 if success else 1)
