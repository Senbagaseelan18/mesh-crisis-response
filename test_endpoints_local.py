#!/usr/bin/env python3
"""Test all endpoints"""

import json
from server.app import reset_env, step_env, get_state, get_tasks

print("=" * 70)
print("TESTING ALL ENDPOINTS")
print("=" * 70)

endpoints = [
    ("POST /reset", reset_env),
    ("POST /step", step_env),
    ("GET /state", get_state),
    ("GET /tasks", get_tasks),
]

for name, endpoint_func in endpoints:
    print(f"\n{name}")
    print("-" * 70)
    try:
        result = endpoint_func()
        print(f"✅ Status Code: {result.status_code}")
        body = result.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        print(f"✅ Content-Type: {dict(result.headers).get('content-type', 'N/A')}")
        print(f"✅ Body: {body}")
        
        # Verify JSON is valid
        data = json.loads(body)
        print(f"✅ Valid JSON with keys: {list(data.keys())}")
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("ALL ENDPOINTS TESTED")
print("=" * 70)
