# OpenEnv Submission Debugging Guide

## Status Check ✅

### Local Testing - ALL PASS:
```
✅ POST /reset → HTTP 200 + Valid JSON
✅ POST /step → HTTP 200 + Valid JSON
✅ GET /state → HTTP 200 + Valid JSON
✅ GET /tasks → HTTP 200 + Valid JSON
```

### Git Status - ALL PUSHED:
```
✅ server/app.py → Has main() function, JSONResponse with 200
✅ pyproject.toml → Has [project.scripts] server entry
✅ uv.lock → Created
✅ Dockerfile → At repo root
✅ All committed and pushed to GitHub & HF Spaces
```

### Code Verified:
```
✅ FastAPI running on 0.0.0.0:8000
✅ CORS enabled
✅ All endpoints return proper JSONResponse with status_code=200
✅ Content-Type: application/json correct
```

---

## If Still Failing on OpenEnv Submit:

### Step 1: Check HF Space Status
1. Go to: https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router
2. Look at the status:
   - **Green "Running"** → Space is live
   - **Yellow "Building"** → Still deploying (wait 5-10 minutes)
   - **Red "Error"** → Deployment failed (check logs)

### Step 2: Test HF Space Manually
```bash
# Test if space responds to POST /reset
curl -X POST -H "Content-Type: application/json" -d '{}' \
  https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router/reset

# Should return HTTP 200 with JSON like:
# {"observation":{"state":0,"battery":100.0,"hops":0},"reward":0.0,"done":false}
```

### Step 3: Verify Submission URL
The OpenEnv form asks for the HF Space URL. Make sure it's:
```
https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router
```
NOT:
```
https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router/  (with trailing slash)
```

### Step 4: Wait & Re-submit
If HF Space was still building, wait 10 minutes then:
1. Go to OpenEnv: https://openenv.com/h/openenvhackathon
2. Click "Update Submission"
3. Enter fresh URLs
4. Click "Submit"

---

## If HF Space Shows "Error":

### Check HF Space Logs:
1. Go to: https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router
2. Click "Logs" tab
3. Look for error messages in:
   - **container** logs
   - **build** logs

### Common Issues & Fixes:

**If Docker build failed:**
- Dockerfile might have issues with package installation
- Make sure only FastAPI and Uvicorn are required

**If server crashes on startup:**
- Check server/app.py for import errors
- Verify main() function exists
- Check pyproject.toml [project.scripts] is correct

---

## Exact URL for OpenEnv Submission:

**GitHub URL:**
```
https://github.com/Senbagaseelan18/mesh-crisis-response
```

**HF Spaces URL:**
```
https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router
```

---

## If Still Stuck:

1. **Manually test locally one more time:**
   ```bash
   python test_endpoints_local.py
   ```

2. **Check all files exist:**
   - server/app.py (with main() function)
   - pyproject.toml (with [project.scripts])
   - uv.lock (exists)
   - Dockerfile (at repo root)

3. **Force push if needed:**
   ```bash
   git push -f origin main
   git push -f huggingface main
   ```

4. **Wait full 15-20 minutes for HF Space rebuild**

5. **Then re-submit to OpenEnv**
