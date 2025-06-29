# 🇮🇳 India Crime Analytics Dashboard

A modern, interactive Streamlit dashboard for analyzing crime patterns and trends across Indian states using NCRB data (2020-2022).

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard Overview](screenshots/dashboard_overview.png)

### State-wise Crime Distribution
![State-wise Crime Distribution](screenshots/statewise_distribution.png)

### State Filter Example
![State Filter Example](screenshots/state_filter_example.png)

---

## 🚀 Features
- Clean, dark-themed UI with glassmorphism KPI cards
- Interactive filters for year and state
- Dynamic KPI cards (total crimes, highest crime state, crime rate, chargesheet rate, etc.)
- Crime trend line chart and state-wise bar chart
- Geographical choropleth map for state-wise crime analysis
- Responsive layout for desktop and mobile

---

## 🗂️ Project Structure
```
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── ncrb_crime_data/      # NCRB CSV data
├── screenshots/          # App screenshots for README
└── ...
```

---

## 🛠️ Setup & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/india-crime-dashboard.git
   cd india-crime-dashboard
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. **Open in browser:**
   Visit [http://localhost:8501](http://localhost:8501)

---

## 📊 Data Source
- [National Crime Records Bureau (NCRB)](https://ncrb.gov.in/) 2020-2022

---

## 🙏 Credits
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)
- [NCRB](https://ncrb.gov.in/)

---

## 📄 License
MIT License

---

> **Note:** Replace the screenshot file names and update the GitHub repo URL as needed. Place your screenshots in a `screenshots/` folder at the project root.
