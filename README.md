Adaptive Allocator – Memory Allocation Visualizer
📌 Overview

Adaptive Allocator is a Python + Flask–based mini-project that demonstrates various memory allocation strategies such as:

-> First Fit

-> Best Fit

-> Worst Fit

-> Next Fit

It helps visualize how memory blocks are assigned to processes in Operating Systems.

🚀 Features

-> Interactive web UI

-> Visual block allocation

-> Supports all major allocation strategies

-> Easy-to-understand diagrams

-> Flask backend with clean APIs

🛠️ Technologies Used
  Component	             Technology
-> Frontend	          -> HTML, CSS, JS
-> Backend	          -> Python (Flask)
-> Tools	          -> Git, GitHub

📂 Project Structure

adaptive_allocator/
│── app.py
│── allocators/
│   ├── first_fit.py
│   ├── best_fit.py
│   ├── worst_fit.py
│   └── next_fit.py
│── static/
│── templates/
└── README.md

▶️ How to Run Locally
1. Clone the repo
git clone https://github.com/ig-hraj/adaptive_allocator.git
cd adaptive_allocator

2. Create virtual environment
python -m venv venv

3. Activate venv
.\venv\Scripts\activate

4. Install dependencies
pip install -r requirements.txt

5. Run server
python app.py


## 📌 System Architecture (High-Level)

                ┌─────────────────────────┐
                │      Frontend (HTML)    │
                │  - Dashboard UI         │
                │  - Progress Bars        │
                │  - Threshold Controls   │
                └────────────┬────────────┘
                             │ (API Calls)
                             ▼
                ┌─────────────────────────┐
                │     Flask Backend       │
                │  - /monitor API         │
                │  - /set_thresholds API  │
                │  - Background Thread    │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │  Process Group Manager  │
                │ - psutil monitors CPU   │
                │ - Auto adjust priority  │
                └─────────────────────────┘

