# FinAdvisor AI

Your **personal AI-powered financial advisor**.  
This project provides a web-based platform built with **React (frontend)** and **Flask (backend)** to deliver **personalized financial recommendations** using AI.

## Features

### Frontend (React)
- **Home Page** – Landing page introducing the AI advisor.
- **Profile Page** – Users can input financial details (income, expenses, savings rate, risk tolerance, etc.).
- **Dashboard** – Displays financial metrics, health score, and quick actions.
- **Recommendations** – AI-powered (or fallback mock) personalized investment & budgeting strategies.
- **Responsive Design** – Optimized for desktop & mobile.

### Backend (Flask)
- **Profile API** – Receives and stores user profile data.
- **Recommendation API** – Generates AI-based recommendations or mock data if ML service is offline.
- **System Status API** – Monitors backend health.
- **CORS Enabled** – Works seamlessly with frontend running on a different port.

## Tech Stack

**Frontend:**
- React (Vite or CRA)
- React Router
- Axios

**Backend:**
- Flask
- Flask-CORS
- Pandas & Numpy (for data processing)

## Installation

### 1. Clone the Repository
```
bash
git clone https://github.com/your-username/finadvisor-ai.git
cd finadvisor-ai
```
### 2. Setup Backend
```
cd back-end
python -m venv venv        # (Optional but recommended)
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python app.py
```

The backend runs on http://localhost:5000

### 3. Setup Frontend
```
cd ../front-end
npm install
npm run dev
```

The frontend runs on http://localhost:5173 (Vite default)

## Usage
1. Go to http://localhost:5173
2. Create your financial profile.
3. View your dashboard for financial insights.
4. Generate AI-powered recommendations.

## Known Issues
pip install numpy may fail with Python 3.12. Use Python 3.11 or install wheels:
```
pip install numpy==1.24.3 --only-binary :all:
```

## License
MIT License – Free to use and modify.

## Contributing
Pull requests are welcome. For major changes, please open an issue first.



