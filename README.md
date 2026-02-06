# 🏏 IPL Analytics Platform

## End-to-end Data Analytics Solution for IPL Cricket Data

[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white&logoWidth=40)](https://www.snowflake.com/)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white&logoWidth=40)](https://www.getdbt.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&logoWidth=40)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&logoWidth=40)](https://www.python.org/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-blue?style=for-the-badge&logo=streamlit&logoColor=white&logoWidth=40)](https://aakashdoraisamy-ipl-analytics-dbt-snowflak-dashboardsapp-m5wq2s.streamlit.app/)


---

## 📖 Overview

A production-grade data pipeline that analyzes **13 seasons of IPL cricket** (2008–2020), processing over **179,000 ball-by-ball records** across **756 matches**. The platform demonstrates modern data engineering practices with cloud-native technologies, transforming raw cricket data into actionable insights via interactive dashboards.

### Key Features
- End-to-end automated data pipeline
- Multi-layered architecture (Raw → Staging → Analytics)
- Interactive Streamlit dashboard
- Comprehensive data quality tests
- Player and team performance analytics

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Warehouse** | Snowflake | Cloud storage and compute engine |
| **Transformations** | dbt | SQL-based data modeling and testing |
| **Visualization** | Streamlit + Plotly | Interactive dashboards and charts |
| **Languages** | SQL, Python | Data processing and application logic |

---

## 📊 Data Models

### Staging Layer
- **stg_deliveries**: Cleaned ball-by-ball records with match phases  
- **stg_matches**: Standardized match information  

### Analytics Layer
- **fct_batting_performance**: Player batting metrics per match  
- **fct_bowling_performance**: Player bowling metrics per match  
- **fct_team_performance**: Team-level statistics and outcomes  

---

## 🎨 Dashboard Features
- **Key Metrics**: Matches, deliveries, players, teams, sixes  
- **Top Performers**: Run scorers and wicket takers  
- **Advanced Analytics**: Phase-wise scoring, batting vs chasing analysis  
- **Team Comparison**: Win percentages, scoring averages  
- **Interactive Filters**: Season selection, dynamic updates  

---

## 💡 Key Insights

- Teams winning toss have **52% match win rate**  
- Scoring 50+ in powerplay leads to **65% win rate**  
- Death overs economy strongly correlates with outcomes  
- Chasing success rate increased to **60%** in recent seasons  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Snowflake account 

### Setup

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/ipl-analytics-project.git
cd ipl-analytics-project
```

2. **Snowflake Setup**
- Execute SQL scripts in `snowflake/` folder
- Load CSV files into tables

3. **dbt Configuration**
```bash
cd dbt_ipl
pip install dbt-snowflake
dbt run
dbt test
```

4. **Launch Dashboard**
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔮 Future Enhancements

- Match outcome prediction (ML)
- Real-time data ingestion
- Player comparison tool
- Fantasy team optimizer
- REST API development

---
<div align="center">

</div>
