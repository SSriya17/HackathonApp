# 🚀 Complete Guide: Push to GitHub + Run Dashboard

## Part 1: Push to GitHub (Step-by-Step)

### Step 1: Open Terminal
- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Press `Win + R`, type "cmd", press Enter

### Step 2: Navigate to Your Project
Copy and paste this command:
```bash
cd /Users/sreya/Desktop/HackathonApp-main
```

### Step 3: Check if Git is Installed
```bash
git --version
```
**If you see a version number** → Good! Continue to Step 4  
**If you see "command not found"** → Install Git first:
- Mac: `xcode-select --install`
- Or download from: https://git-scm.com/downloads

### Step 4: Initialize Git (First Time Only)
```bash
git init
```
**Output should say:** "Initialized empty Git repository..."

### Step 5: Check What Files Will Be Uploaded
```bash
git status
```
**You should see your files listed.** Make sure `venv/` is NOT listed (it should be ignored).

### Step 6: Add All Files
```bash
git add .
```

### Step 7: Verify Files Are Staged
```bash
git status
```
**You should see:** "Changes to be committed" with a list of files.

### Step 8: Create Your First Commit
```bash
git commit -m "Initial commit: Telecom Complaints Dashboard"
```

### Step 9: Create Repository on GitHub Website

1. **Go to GitHub**: https://github.com
2. **Sign in** (or create account if needed)
3. **Click the "+" icon** in top right corner
4. **Click "New repository"**
5. **Repository name**: `HackathonApp-main` (or any name you want)
6. **Description** (optional): "Telecom Complaints Dashboard"
7. **Visibility**: Choose Public or Private
8. **IMPORTANT**: Do NOT check any boxes (no README, no .gitignore, no license)
9. **Click "Create repository"**

### Step 10: Copy Your Repository URL
After creating the repository, GitHub will show you a URL like:
```
https://github.com/YOUR_USERNAME/HackathonApp-main.git
```
**Copy this URL!** You'll need it in the next step.

### Step 11: Connect Local Repository to GitHub
Replace `YOUR_USERNAME` with your actual GitHub username:
```bash
git remote add origin https://github.com/YOUR_USERNAME/HackathonApp-main.git
```

**Example:**
```bash
git remote add origin https://github.com/sreyagudipati/HackathonApp-main.git
```

### Step 12: Push to GitHub
```bash
git branch -M main
git push -u origin main
```

**If asked for credentials:**
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (NOT your password!)
  - Get token: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Check "repo" scope
  - Copy the token and use it as password

### Step 13: Verify Upload
Go to your GitHub repository in browser and check that all files are there!

---

## Part 2: Run the Dashboard (Step-by-Step)

### Step 1: Open Terminal
- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter

### Step 2: Navigate to Your Project
```bash
cd /Users/sreya/Desktop/HackathonApp-main
```

### Step 3: Activate Virtual Environment (If You Have One)
```bash
source venv/bin/activate
```
**You should see `(venv)` appear at the start of your terminal prompt.**

**If you don't have a venv**, skip this step and continue to Step 4.

### Step 4: Install Dependencies (First Time Only)
```bash
pip install -r frontend/requirements.txt
```

**Wait for installation to complete...** This may take 1-2 minutes.

**Expected output:**
```
Collecting streamlit...
Collecting pandas...
Installing collected packages...
Successfully installed streamlit-1.28.0 pandas-2.0.0 ...
```

### Step 5: Verify Streamlit is Installed
```bash
streamlit --version
```

**You should see:** `Streamlit, version X.X.X`

### Step 6: Run the Dashboard
```bash
streamlit run frontend/dashboard.py
```

### Step 7: Dashboard Opens!
- **Browser should open automatically**
- **If not**, manually go to: `http://localhost:8501`
- **You should see the dashboard!**

### Step 8: Use the Dashboard
1. **Upload a CSV file** using the sidebar
2. **Explore categories** by selecting from dropdown
3. **View charts and insights**
4. **Use AI chatbot** (enter OpenAI API key if you have one)

### Step 9: Stop the Dashboard (When Done)
Press `Ctrl + C` in the terminal

---

## Complete Terminal Session Example

Here's what your complete session will look like:

```bash
# ============================================
# PART 1: PUSH TO GITHUB
# ============================================

# Step 2: Navigate
$ cd /Users/sreya/Desktop/HackathonApp-main

# Step 3: Check Git
$ git --version
git version 2.39.0

# Step 4: Initialize (first time only)
$ git init
Initialized empty Git repository in /Users/sreya/Desktop/HackathonApp-main/.git

# Step 5: Check status
$ git status
On branch main
Untracked files:
  frontend/
  backend/
  data/
  ...

# Step 6: Add files
$ git add .

# Step 7: Check staged files
$ git status
Changes to be committed:
  new file: frontend/dashboard.py
  new file: backend/backend.py
  ...

# Step 8: Commit
$ git commit -m "Initial commit: Telecom Complaints Dashboard"
[main (root-commit) abc1234] Initial commit: Telecom Complaints Dashboard
 15 files changed, 1234 insertions(+)

# Step 11: Add remote (replace YOUR_USERNAME)
$ git remote add origin https://github.com/YOUR_USERNAME/HackathonApp-main.git

# Step 12: Push
$ git branch -M main
$ git push -u origin main
Enumerating objects: 15, done.
Writing objects: 100% (15/15), done.
To https://github.com/YOUR_USERNAME/HackathonApp-main.git
 * [new branch]      main -> main

# ============================================
# PART 2: RUN DASHBOARD
# ============================================

# Step 2: Navigate (if in new terminal)
$ cd /Users/sreya/Desktop/HackathonApp-main

# Step 3: Activate venv
$ source venv/bin/activate
(venv) $ 

# Step 4: Install dependencies (first time)
(venv) $ pip install -r frontend/requirements.txt
Collecting streamlit...
Successfully installed streamlit-1.28.0 ...

# Step 5: Verify
(venv) $ streamlit --version
Streamlit, version 1.28.0

# Step 6: Run dashboard
(venv) $ streamlit run frontend/dashboard.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501

# Dashboard opens in browser!

# Step 9: Stop (when done)
# Press: Ctrl + C
```

---

## Quick Reference: Copy-Paste Commands

### Push to GitHub (All at Once)
```bash
cd /Users/sreya/Desktop/HackathonApp-main
git init
git add .
git commit -m "Initial commit: Telecom Complaints Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/HackathonApp-main.git
git branch -M main
git push -u origin main
```

### Run Dashboard (All at Once)
```bash
cd /Users/sreya/Desktop/HackathonApp-main
source venv/bin/activate
pip install -r frontend/requirements.txt
streamlit run frontend/dashboard.py
```

---

## Troubleshooting

### Git Issues

**Error: "git: command not found"**
```bash
# Mac: Install Xcode Command Line Tools
xcode-select --install
```

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/HackathonApp-main.git
```

**Error: "Authentication failed"**
- Use Personal Access Token instead of password
- Get token: https://github.com/settings/tokens
- Or use GitHub CLI: `gh auth login`

### Running Issues

**Error: "streamlit: command not found"**
```bash
pip install streamlit
```

**Error: "ModuleNotFoundError"**
```bash
pip install -r frontend/requirements.txt
```

**Error: "Port already in use"**
```bash
streamlit run frontend/dashboard.py --server.port 8502
```

**Error: "Backend not available"**
- Make sure `backend/` folder exists in project root
- Check that `backend/__init__.py` exists

---

## Next Steps After Running

1. ✅ **Upload a CSV file** with complaint data
2. ✅ **Explore categories** by clicking on the chart
3. ✅ **View PM recommendations** for each category
4. ✅ **Use AI chatbot** (optional, requires OpenAI API key)

---

## Summary Checklist

### GitHub Push:
- [ ] Open Terminal
- [ ] Navigate to project: `cd /Users/sreya/Desktop/HackathonApp-main`
- [ ] Initialize git: `git init`
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit"`
- [ ] Create repository on GitHub website
- [ ] Add remote: `git remote add origin [URL]`
- [ ] Push: `git push -u origin main`

### Run Dashboard:
- [ ] Open Terminal
- [ ] Navigate: `cd /Users/sreya/Desktop/HackathonApp-main`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install: `pip install -r frontend/requirements.txt`
- [ ] Run: `streamlit run frontend/dashboard.py`
- [ ] Open browser to http://localhost:8501

---

**You're all set! 🎉**


