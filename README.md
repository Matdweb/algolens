# AlgoLens — Algorithm Complexity Visualizer (Django + Python + Plotly)

**A web app that benchmarks algorithms and visualizes their runtime growth (Big-O) with a retro BIOS-style UI.**  
Built with Django, Plotly, and simple Python benchmarking utilities — containerized with Docker for easy sharing and demoing.

---

## 🎯 What It Does

- Run micro-benchmarks for predefined algorithms (bubble, merge, quick, linear search, binary search).  
- Measure real runtimes with `time.perf_counter()` and plot **measured** vs **theoretical** (scaled) curves.  
- Retro **BIOS-style** UI (pure CSS) for an eye-catching aesthetic.  
- Users can **signup / login**, run benchmarks and **save results** to their account.  
- Optional: users can paste small **custom algorithm functions** (limited, sanitized) to benchmark for demo purposes.  
- Dockerized for one-command demos.

---

## 💡 Why This Project Matters

- **Unique & memorable UI** (BIOS theme) — stands out among CRUD apps.  
- Demonstrates strong **Python + Django + data visualization** skills.  
- Shows practical understanding of **algorithmic complexity** and performance benchmarking.  
- Highlights backend, data, and dev-ops capabilities all in one clean project.  
- Lightweight, extendable, and perfect for short portfolio videos or interviews.

---

## 🔧 Tech Stack

- **Backend:** Django (5.x), Python (3.12+)  
- **Data Processing:** pandas, numpy  
- **Visualization:** Plotly (interactive charts)  
- **Deployment:** Docker / Docker Compose  
- **UI:** Pure CSS, BIOS-themed design  
- **Database:** SQLite (default), easily swappable with Postgres  

**Key files:**
- bench/algorithms.py — algorithm implementations  
- bench/benchmark.py — benchmark logic (timing + averaging)  
- bench/views.py — form, benchmark orchestration, Plotly chart generation  
- bench/templates/bench/*.html — BIOS-themed templates  
- bench/static/bench/bios.css — retro BIOS stylesheet  
- Dockerfile, docker-compose.yml, requirements.txt

---

## 🚀 Quickstart (Using Docker)

> Recommended for easiest setup and zero dependency installation.

### 1. Build and start the container
~~~
docker compose build
docker compose up -d
~~~

### 2. Run database migrations
~~~
docker compose run --rm web python manage.py migrate
~~~

### 3. Create a superuser for /admin/
~~~
docker compose run --rm web python manage.py createsuperuser
~~~

### 4. Access the app
- **App:** http://localhost:8000/  
- **Admin Panel:** http://localhost:8000/admin/

### 5. Stop
~~~
docker compose down
~~~

---

## 🧰 Quickstart (Without Docker)

### 1. Create virtual environment and install dependencies
~~~
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
~~~

### 2. Migrate and create admin user
~~~
python manage.py migrate
python manage.py createsuperuser
~~~

### 3. Run development server
~~~
python manage.py runserver
# Then open http://127.0.0.1:8000/
~~~

---

## 🧭 How to Use

1. Open the home page (/).  
2. **Signup or Login** from the top links.  
3. Select an algorithm, input sizes (e.g. 100,500,1000), and number of repeats.  
4. Click **Run Benchmark**.  
5. View an interactive Plotly chart in BIOS theme and raw results.  
6. Logged-in users have benchmarks **auto-saved** to their history page (/history/).  
7. Admins can view all benchmarks in /admin/.

---

## 🎨 BIOS Theme (Plotly Customization)

The Plotly charts have been styled to match the BIOS UI — black background, neon green lines, and monospace fonts.

If you’d like to tweak the theme, edit this section in views.py:
~~~
fig.update_layout(
    paper_bgcolor='#000',
    plot_bgcolor='#000',
    font=dict(family='Courier New, monospace', color='#0f0', size=14),
    xaxis=dict(color='#0f0', gridcolor='#0a0', zerolinecolor='#0f0'),
    yaxis=dict(color='#0f0', gridcolor='#0a0', zerolinecolor='#0f0'),
)
~~~

---

## ⚠️ Security Notes

This project supports **user-submitted code** for demonstration only.  
A simple validation step blocks dangerous keywords (import, os, sys, eval, exec, etc.), and execution runs in a restricted environment.

However:
- ⚠️ **Not safe for production** — do not deploy this publicly as-is.  
- Designed purely for **portfolio demos and educational showcases**.  

To make it production-ready, you'd need proper sandboxing (isolated container/process per job, CPU/memory limits, timeouts, etc.).

---

## 🧪 Tests

Run the small included test suite:
~~~
python manage.py test bench
~~~

---

## 📁 Useful Commands Recap

~~~
python manage.py migrate                # Apply DB migrations
python manage.py createsuperuser        # Create admin
python manage.py runserver              # Run local dev server
docker compose up --build -d            # Build & run in Docker
docker compose run --rm web python manage.py migrate  # Run migrations in container
~~~

## 🤝 Contributing

Pull requests are welcome!  
If you extend AlgoLens, please:
- Keep the BIOS theme consistent (bios.css)  
- Add minimal tests for new logic  
- Document new features in the README  

---

## 📜 License

MIT License — fre# AlgoLens — Algorithm Complexity Visualizer (Django + Python + Plotly)

**A small, portfolio-ready web app that benchmarks algorithms and visualizes their runtime growth (Big-O) with a retro BIOS-style UI.**  
Built with Django, Plotly, and simple Python benchmarking utilities — containerized with Docker for easy sharing and demoing.

---
🧩 Project by [Matias Vargas](https://mat-dweb.lovable.app/)  
*“AlgoLens: Visualizing algorithms the retro way.”*
