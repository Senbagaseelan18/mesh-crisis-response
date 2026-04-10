# 🚀 Deploying to Hugging Face Spaces

This guide explains how to deploy the Emergency Mesh-Network Router to Hugging Face Spaces.

## Quick Setup for HF Spaces

### Option 1: Update Existing Space (If Already Created)

If you already have a HF Space at `https://huggingface.co/spaces/nishahak/emergency-mesh-router`, follow these steps:

**Step 1: Add HF Spaces Remote**
```bash
# Add the HF Spaces git remote
git remote add huggingface https://huggingface.co/spaces/nishahak/emergency-mesh-router

# Verify the remote is added
git remote -v
```

**Step 2: Push to HF Spaces**
```bash
# Push the code to HF Spaces
git push huggingface main

# Or if your main branch has a different name:
git push huggingface <your_branch>:main
```

**Step 3: Monitor Deployment**
- Go to your Space: https://huggingface.co/spaces/nishahak/emergency-mesh-router
- Check the logs for build status
- Wait for the Docker container to build and deploy (usually 2-5 minutes)
- The Space should auto-restart with the new code

### Option 2: Create New Space (If Not Already Created)

**Step 1: Create Space on HuggingFace**
1. Go to https://huggingface.co/new-space
2. Select **Space name**: `emergency-mesh-router`
3. Select **Space SDK**: `Docker`
4. Choose visibility: **Public** (recommended for hackathon)
5. Click **Create Space**

**Step 2: Clone the Space Repository**
```bash
# Clone the empty HF Space (you'll be given a Git URL)
git clone https://huggingface.co/spaces/<your-username>/emergency-mesh-router hf_space
cd hf_space
```

**Step 3: Copy Project Files**
```bash
# Copy your project files (preserving structure)
cp -r ~/Open_env/* .
# Excluding .git folder
rm -rf .git/
```

**Step 4: Configure for HF Spaces**
Make sure these files are in the root:
- ✅ `Dockerfile`
- ✅ `requirements.txt`
- ✅ `openenv.yaml`
- ✅ `server/` folder
- ✅ `agents/` folder
- ✅ All other project files

**Step 5: Push to HF Spaces**
```bash
git add .
git commit -m "Initial deployment to HF Spaces"
git push origin main
```

## Verifying the Deployment

Once deployed, the Space runs at: `https://huggingface.co/spaces/<username>/emergency-mesh-router`

**Test the endpoints:**
```bash
# From your local machine, test against the HF Space URL:
python test_endpoints.py https://<username>-emergency-mesh-router.hf.space

# Or test specific endpoint:
curl -X POST https://<username>-emergency-mesh-router.hf.space/reset
```

Expected response:
```json
{
  "detail": "Environment reset successfully",
  "observation": {...},
  "difficulty": "easy",
  "max_hops": 5
}
```

## Troubleshooting

### Space Not Starting
- Check Space logs in HF interface (Settings → Logs)
- Common issues:
  - Missing `Dockerfile` at root
  - Missing dependencies in `requirements.txt`
  - Port 7860 not exposed (HF Spaces uses port 7860, not 8000)

### Port Configuration
HF Spaces uses port **7860** by default. If your app expects port 8000, you can:

**Option A: Update Dockerfile for HF Spaces**
```dockerfile
# At the bottom of Dockerfile, change the CMD line:
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
```

**Option B: Let HF Spaces proxy requests**
- HF automatically proxies requests to port 8000 if available
- No changes needed, your Dockerfile is fine

### Endpoint Returns 404
- Space might still be building (check logs)
- Code might not have deployed yet (refresh in 30 seconds)
- Dockerfile might not have latest code
- **Solution**: Push updated code again with `git push huggingface main`

## Useful Commands

```bash
# Check current remotes
git remote -v

# Push to specific remote
git push huggingface main

# View Space settings
Visit: https://huggingface.co/spaces/<username>/emergency-mesh-router/settings

# View Space logs
Visit: https://huggingface.co/spaces/<username>/emergency-mesh-router/logs

# Restart the Space
Visit: Settings → Restart Space
```

## SSH Setup (Optional, for easier pushes)

```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add SSH key to HuggingFace account
# Visit: https://huggingface.co/settings/keys

# Use SSH for git remote
git remote set-url huggingface git@huggingface.co:spaces/<username>/emergency-mesh-router
```

## Current Status

| Component | Status | Location |
|-----------|--------|----------|
| GitHub Code | ✅ Deployed | https://github.com/Senbagaseelan18/mesh-crisis-response |
| HF Spaces | ⚠️ Needs Update | https://huggingface.co/spaces/nishahak/emergency-mesh-router |
| OpenEnv Submission | ❌ Pending | Waiting for HF Spaces update |

## Next Steps

1. **Update HF Spaces** with the latest code (use Option 1 above)
2. **Wait 2-5 minutes** for Docker build to complete
3. **Test endpoints**: `python test_endpoints.py https://<username>-emergency-mesh-router.hf.space`
4. **Re-submit** to OpenEnv platform
5. Phase 1 validation should now pass ✅

---

**Need Help?**
- HF Spaces Docs: https://huggingface.co/docs/hub/spaces
- OpenEnv Support: help_openenvhackathon@scaler.com
