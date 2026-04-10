# 🔑 Hugging Face Spaces - Authorization & Deployment Guide

## Problem
You don't have push access to `nishahak/emergency-mesh-router` Space. This is because:
- The Space is owned by nishahak's account
- You need to either: (1) Get collaborator access, or (2) Create your own Space

---

## Option A: nishahak Updates Space (Recommended for Teams)

**Have nishahak run these commands:**

```bash
# Clone the HF Space
git clone https://huggingface.co/spaces/nishahak/emergency-mesh-router
cd emergency-mesh-router

# Add GitHub as remote
git remote add github https://github.com/Senbagaseelan18/mesh-crisis-response

# Pull latest code from GitHub (use -X ours to prefer local HF files if conflicts)
git pull github main --allow-unrelated-histories -X ours --no-edit

# Push to HF Space
git push origin main
```

**Result:** HF Space updates with latest code ✅

---

## Option B: Create Your Own Space (Independent)

### Step 1: Create Space on Hugging Face
1. Go to: https://huggingface.co/new-space
2. **Space name**: emergency-mesh-router (or your variant)
3. **Space SDK**: Docker
4. **Visibility**: Public
5. Click "Create Space"

### Step 2: Configure Git Remote
```bash
# Replace <your-username> with your actual HF username
git remote remove huggingface  # Remove old remote
git remote add huggingface https://huggingface.co/spaces/<your-username>/emergency-mesh-router
```

### Step 3: Push Code
```bash
git push -f huggingface main
```

### Step 4: Update OpenEnv Submission
After Space builds (2-5 minutes):
1. Go to OpenEnv submission
2. Update HF Spaces URL to: `https://huggingface.co/spaces/<your-username>/emergency-mesh-router`
3. Re-submit

---

## How to Check Your HF Username

Visit: https://huggingface.co/settings/account

The URL format is: `https://huggingface.co/<your-username>`

Example: If you see `https://huggingface.co/settings/account` and your profile is at `https://huggingface.co/senba`, your username is **senba**

---

## Quickstart Commands

### For Option A (nishahak's Space):
```bash
# This command for nishahak to run
git clone https://huggingface.co/spaces/nishahak/emergency-mesh-router && \
cd emergency-mesh-router && \
git remote add github https://github.com/Senbagaseelan18/mesh-crisis-response && \
git pull github main --allow-unrelated-histories -X ours --no-edit && \
git push origin main
```

### For Option B (Your Space):
Replace `<your-username>` with your HF username:
```bash
git remote remove huggingface
git remote add huggingface https://huggingface.co/spaces/<your-username>/emergency-mesh-router
git push -f huggingface main
```

---

## Current Status

| Scenario | Action | Timeline |
|----------|--------|----------|
| **Option A (nishahak)** | nishahak runs git commands | 2-5 min build time |
| **Option B (Your Space)** | Create new Space + push | 5-10 min total |
| **After Either** | Re-submit to OpenEnv | Immediate |

---

## Which Option Should We Use?

**Choose Option A if:**
- nishahak is available to help
- You want to keep single Space URL
- Team wants centralized deployment

**Choose Option B if:**
- nishahak is not immediately available
- You prefer independent Space
- Want to proceed without waiting

---

**What's your HF username?** We can proceed with Option B immediately!
