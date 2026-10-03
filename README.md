# 🏥 Patient Care Analytics — End-to-End Healthcare Data Analysis

> A complete **SQL + Python + Streamlit** data analytics project built to demonstrate real-world healthcare business intelligence — from raw data to interactive dashboards.

![SQL](https://img.shields.io/badge/SQL-MySQL-blue?logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-green?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/Reporting-Power%20BI-yellow?logo=powerbi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📌 Project Overview

This project analyzes hospital operations data to generate **actionable business insights** for healthcare decision-makers. It covers patient demographics, appointment trends, doctor performance, treatment costs, billing patterns, and revenue analysis.

### What makes this different from a typical SQL project?

| Feature | Typical SQL Project | This Project |
|---------|-------------------|-------------|
| **Queries** | Basic SELECT, COUNT | 40+ queries across 3 difficulty levels |
| **Schema** | No design | Proper ERD with primary/foreign keys |
| **Data** | Tiny sample | 300 patients, 800 appointments, 500 treatments |
| **Visualization** | None | Interactive Streamlit dashboard + charts |
| **Business Value** | Simple counts | KPIs, no-show rates, revenue by doctor, cohort analysis |
| **Hosting** | Local only | Deployed on Streamlit Cloud |

---

## 🗂 Project Structure

```
patient-care-analytics/
│
├── 📁 data/raw/                  # Raw CSV datasets
│   ├── patients.csv              # 300 patient records
│   ├── doctors.csv               # 30 doctor profiles
│   ├── appointments.csv          # 800 appointment records
│   ├── treatments.csv            # 500 treatment records
│   └── billing.csv               # 500 billing records
│
├── 📁 sql/                       # SQL query files (MySQL syntax)
│   ├── 01_schema.sql             # Database schema with keys & constraints
│   ├── 02_basic_queries.sql      # 15 foundational queries
│   ├── 03_intermediate_queries.sql # 15 queries with JOINs & CASE
│   └── 04_advanced_queries.sql   # 10 queries with CTEs & window functions
│
├── 📁 python/                    # Python scripts
│   ├── data_generator.py         # Script to generate sample data
│   └── eda_analysis.py           # Exploratory Data Analysis + chart export
│
├── 📁 app/                       # Streamlit web dashboard
│   └── streamlit_app.py          # Interactive 4-tab analytics dashboard
│
├── 📁 docs/                      # Generated charts and documentation
├── 📁 dashboard/screenshots/     # Dashboard screenshots
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🗄 Database Schema (ERD)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PATIENTS   │     │   DOCTORS    │     │  TREATMENTS  │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ patient_id   │─┐   │ doctor_id    │─┐   │ treatment_id │─┐
│ first_name   │ │   │ first_name   │ │   │ appointment_id│ │
│ last_name    │ │   │ last_name    │ │   │ treatment_type│ │
│ gender       │ │   │ specialization│ │  │ treatment_date│ │
│ age          │ │   │ years_exp    │ │   │ cost         │ │
│ phone        │ │   │ phone        │ │   └──────────────┘ │
│ address      │ │   │ consult_fee  │ │                    │
│ blood_group  │ │   └──────────────┘ │                    │
│ reg_date     │ │                    │                    │
└──────────────┘ │   ┌──────────────┐ │   ┌──────────────┐ │
                 │   │ APPOINTMENTS │ │   │   BILLING    │ │
                 └──▶├──────────────┤◀┘   ├──────────────┤ │
                     │ appointment_id│──▶ │ billing_id   │ │
                     │ patient_id   │    │ patient_id   │◀┘
                     │ doctor_id    │    │ treatment_id │
                     │ appt_date    │    │ total_amount │
                     │ appt_time    │    │ discount     │
                     │ status       │    │ final_amount │
                     └──────────────┘    │ pay_status   │
                                         │ pay_date     │
                                         └──────────────┘
```

**5 tables | 3 foreign key relationships | Normalized design**

---

## 🔍 SQL Concepts Demonstrated

### Basic Queries (02_basic_queries.sql)
| Concept | Example |
|---------|---------|
| `SELECT`, `WHERE` | Filter recent appointments |
| `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | Aggregate patient/treatment stats |
| `GROUP BY` + `ORDER BY` | City-wise patient distribution |
| `LIMIT` + `OFFSET` | Top N results |
| `CASE WHEN` | Age group segmentation |
| Date Functions | Monthly appointment trends |

### Intermediate Queries (03_intermediate_queries.sql)
| Concept | Example |
|---------|---------|
| `INNER JOIN` (2-4 tables) | Revenue per doctor across 4 tables |
| `LEFT JOIN` | Find patients with zero appointments |
| Conditional Aggregation | No-show rate using `CASE` inside `SUM` |
| `HAVING` | Filter groups by aggregate condition |
| `DAYNAME()` | Day-of-week analysis |
| Revenue Buckets | Classify bills as Low/Medium/High |

### Advanced Queries (04_advanced_queries.sql)
| Concept | Example |
|---------|---------|
| **CTE** (Common Table Expression) | Monthly revenue trend, visit frequency |
| **RANK()** | Top 3 doctors by revenue |
| **DENSE_RANK()** | Top patients by spend |
| **Running Total** | Cumulative revenue over months |
| **Subquery** (correlated) | Above-average bill detection |
| **Cohort Analysis** | Patient retention (2+ visits) |

---

## 📊 Key Business Insights Generated

1. **Patient Acquisition**: Registration patterns reveal seasonal trends and marketing effectiveness
2. **No-Show Analysis**: Identified doctor-specific no-show rates to optimize scheduling
3. **Revenue per Doctor**: Traced revenue from doctor → appointment → treatment → billing (4-table JOIN)
4. **Patient Retention**: Classified patients as One-time / Regular / Frequent visitors
5. **Peak Hours**: Day-of-week analysis for staffing optimization
6. **Treatment Economics**: Min/Max/Avg costs by treatment type for pricing strategy
7. **Collection Rate**: Payment status breakdown to flag pending collections
8. **City-wise Revenue**: Geographic revenue distribution for expansion planning
9. **Above-Average Bills**: Anomaly detection for billing audit
10. **Year-over-Year Growth**: Annual appointment volume comparison for stakeholders

---

## 🖥 Interactive Dashboard (Streamlit)

The Streamlit app provides a 4-tab interactive dashboard:

| Tab | What it shows |
|-----|--------------|
| **📋 Overview** | KPI cards, monthly trends, appointment status distribution |
| **👥 Patient Insights** | Gender split, age groups, top cities, blood groups |
| **👨‍⚕️ Doctor Performance** | Revenue by doctor, appointments by specialization, no-show rates |
| **💰 Financial Analytics** | Revenue trends, treatment costs, payment status, top bills |

### How to run locally:

```bash
# 1. Clone the repo
git clone https://github.com/akash-2301/patient-care-analytics.git
cd patient-care-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data (if not already present)
cd python
python data_generator.py
cd ..

# 4. Launch the dashboard
streamlit run app/streamlit_app.py
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Database** | MySQL (schema) / SQLite (portable) |
| **Query Language** | SQL (40+ queries) |
| **Data Processing** | Python, Pandas |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Dashboard** | Streamlit |
| **Reporting** | Power BI |
| **Version Control** | Git, GitHub |

---

## 🚀 How to Use This Project

### For SQL Practice
1. Open any file in the `sql/` folder
2. Run queries in MySQL Workbench or any SQL client
3. Use the CSVs in `data/raw/` to load data into your database

### For Dashboard
1. Run the Streamlit app (see instructions above)
2. Use sidebar filters to explore different slices of data

### For EDA Charts
```bash
cd python
python eda_analysis.py
# Charts saved to docs/ folder
```

---

## 📁 Dataset Information

| Table | Records | Description |
|-------|---------|-------------|
| Patients | 300 | Demographics, city, blood group |
| Doctors | 30 | Specialization, experience, fees |
| Appointments | 800 | Date, time, status |
| Treatments | 500 | Type, cost, linked to appointments |
| Billing | 500 | Amounts, discounts, payment status |

> **Note**: Data is synthetically generated with realistic Indian healthcare patterns using `python/data_generator.py`.

---

## 📝 What I Learned

- Writing clean, well-structured SQL queries with proper commenting
- Joining multiple tables to answer complex business questions
- Using CTEs and Window Functions for analytical queries
- Building interactive dashboards with Streamlit and Plotly
- Generating synthetic datasets with Python for testing
- Structuring a data project for portfolio presentation

---

## 👤 Author

**Akash Singh**
- GitHub: [@akash-2301](https://github.com/akash-2301)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/)

---

## ⭐ If you found this useful, give it a star!

This project is open for feedback and suggestions. Feel free to fork, improve, and share.
