# Setup Instructions - Step by Step

## Step 1: Copy the Backend Folder

Copy the entire `backend` folder from `/Users/sreya/Downloads/backend/` to your HackathonApp-main project.

**Your project structure should look like this:**
```
HackathonApp-main/
├── backend/              ← COPY THIS ENTIRE FOLDER HERE
│   ├── __init__.py
│   ├── backend.py
│   ├── data_loader.py
│   ├── categorizer.py
│   ├── data_processor.py
│   ├── requirements.txt
│   ├── example_usage.py
│   └── README.md
├── data/
│   ├── dataset1.csv
│   └── dataset2.csv
├── frontend/
└── requirements.txt
```

## Step 2: Install Dependencies

Open your terminal in the HackathonApp-main folder and run:

```bash
# Activate your virtual environment (if you have one)
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r backend/requirements.txt
```

Or if you want to add to your existing requirements.txt:
```bash
pip install pandas>=2.0.0 numpy>=1.24.0 streamlit>=1.28.0
```

## Step 3: Create Your Streamlit App

Create a file called `app.py` in your HackathonApp-main folder (or in the frontend folder if you prefer).

## Step 4: Test It Works

Run your Streamlit app:
```bash
streamlit run app.py
```

That's it! You're ready to use the backend.

