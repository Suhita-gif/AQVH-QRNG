# AQVH-QRNG
Project: Quantum Random Bit Generator (local)

This repository contains a small Flask backend that produces random bits (optionally via Qiskit Aer) and a simple frontend (`index.html`, `script.js`, `style.css`) that calls the API.

This README explains how to set up the Python environment on Windows (PowerShell), run the backend, serve the frontend locally, test the API, and troubleshoot the errors you reported (connection refused / "Failed to fetch" and matplotlib/tkinter RuntimeError).

1) Quick checklist
- Create and activate a Python virtual environment (recommended).
- Install backend dependencies.
- Start the Flask backend: `backend/app.py` (default: http://127.0.0.1:5000).
- Serve the frontend files from the project root (recommended) or open `index.html` directly.

2) Prerequisites
- Python 3.8+ installed and on PATH.
- (Optional) A working internet connection to pip-install packages.

3) Setup (PowerShell commands)

Open PowerShell and run (commands are separate lines):

    cd C:\Users\Bhargavi\Desktop\aqvh
    python -m venv backend\venv
    # Activate the venv in PowerShell
    & .\backend\venv\Scripts\Activate.ps1
    # Upgrade pip first (optional)
    python -m pip install --upgrade pip
    # Install required packages
    pip install -r backend\requirements.txt

4) Run the Flask backend

With the virtualenv activated (see above), run:

    python backend\app.py

You should see Flask start and bind to 127.0.0.1:5000 by default. Keep this terminal open.

5) Serve the frontend (recommended)

From the project root (not the backend folder), run a simple static HTTP server so the page is served over http:// which avoids some browser restrictions:

    cd C:\Users\Bhargavi\Desktop\aqvh
    python -m http.server 8000

Open http://localhost:8000/index.html in your browser.

6) Quick API smoke tests (PowerShell examples)

# GET generate (quick test)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/generate?num_bits=16" -Method Get

# POST extract (example JSON body)
$body = @{ bits = @(0,1,1,0) } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:5000/extract" -Method Post -Body $body -ContentType 'application/json'

# POST entropy (returns image/png)
Invoke-WebRequest -Uri "http://127.0.0.1:5000/entropy" -Method Post -Body (@{ bits=@(0,1,1,0,0,1) } | ConvertTo-Json) -ContentType 'application/json' -OutFile entropy.png

7) Common errors and fixes

- net::ERR_CONNECTION_REFUSED / "Failed to fetch" in browser console
  - Means the frontend tried to contact the backend but couldn't connect. Check:
    - Is Flask running? Look at the terminal where you started `backend\app.py`.
    - Is it bound to 127.0.0.1:5000? If you changed host/port, update `script.js` or your calls to match.
    - Are you using the same protocol/origin? Serving the frontend at `http://localhost:8000` and backend at `http://127.0.0.1:5000` is fine, but the backend must allow cross-origin requests (see below).

- CORS (Cross-Origin Resource Sharing) issues / "Access to fetch at ... from origin ... has been blocked"
  - The backend includes Flask-CORS support; ensure you installed `flask-cors` and that `backend/app.py` contains `from flask_cors import CORS` and `CORS(app)` near the top.

- RuntimeError: main thread is not in main loop (tkinter / matplotlib errors)
  - This happens when matplotlib uses a GUI backend (tkinter) in a background thread. The backend included with this project should set a non-GUI backend (Agg) so this does not occur. If you still see it, ensure the top of `backend/app.py` sets the matplotlib backend BEFORE importing `matplotlib.pyplot`:

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

8) If you prefer to have Flask serve the UI (single origin)

You can have Flask serve static files so the UI and API share the same origin and avoid CORS entirely. The project already has the UI files at the repo root; to let Flask serve them you can:

- Move `index.html`, `script.js`, `style.css` into `backend/static/` and let Flask serve them, or
- Add a route in `backend/app.py` that uses `send_from_directory` to serve the root `index.html` (not recommended if you want to keep the current layout). If you'd like I can implement this for you.

9) Helpful tips
- If you see `ERR_CONNECTION_REFUSED`, first try to access `http://127.0.0.1:5000/` in the browser — you should get a JSON listing endpoints from the app's index route.
- Open DevTools (F12) -> Network and Console to see request details and full error messages.
- If you installed packages into a system Python but the venv is active, ensure pip installed into the venv by running `pip show flask` and checking the Location path.

10) Next steps I can do for you (pick one)
- Add `CORS(app)` to `backend/app.py` (if missing) and restart the backend.
- Make the Flask app serve the frontend (single origin) and update paths accordingly.
- Add a small health-check endpoint and a sample curl/Powershell test script.
