# 🏥 Healthcare Operations Intelligence

> An enterprise-grade Power BI dashboard analyzing 11,000+ patient admissions across 8 departments and 50 doctors — featuring Dark Theme UI, Star Schema data modeling, Dynamic RLS, DAX measures, and interactive navigation.

---

## 📸 Dashboard Preview

### Page 1 — Operations Overview
![Overview](screenshots/overview.png)

### Page 2 — Doctor Performance
![Doctors](screenshots/doctors.png)

### Page 3 — Financial Overview
![Financial](screenshots/financial.png)

---

## 🎯 Project Objective

Build a healthcare intelligence platform to:
- Monitor patient admissions, wait times, and length of stay across departments
- Identify high readmission risk departments for operational intervention
- Track doctor performance and patient satisfaction
- Analyze revenue, billing status, and financial trends
- Enforce data security through Dynamic Row-Level Security (RLS)

---

## 🔍 Key Insights

| Insight | Finding |
|---|---|
| 🏆 Total Admissions | **11,000+** patients across 4 years |
| 💰 Total Revenue | **$127.96M** across all departments |
| ⚠️ Readmission Rate | **11.70%** — Oncology highest at **17.79%** |
| ⏱️ Avg Wait Time | **45 minutes** overall |
| 🛏️ Avg Length of Stay | **4.50 days** |
| ⭐ Avg Satisfaction | **7.43 / 10** |
| 💳 Payment Status | **59.51% Paid**, 19.8% Partial, 15.62% Pending |
| 🏥 Top Department | Cardiology — highest admissions (1,521) |

---

## 🗂️ Data Model — Star Schema

```
                    ┌─────────────────┐
                    │   dim_date      │
                    │ (Date, Year,    │
                    │  Month, Quarter)│
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────┴────────┐         │        ┌─────────┴────────┐
│ fact_admissions  │         │        │  fact_billing    │
│ (LOS, WaitTime,  │─────────┘        │ (Revenue, Costs, │
│  Diagnosis,      │                  │  PaymentStatus)  │
│  Satisfaction,   │                  └──────────────────┘
│  Readmission)    │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───┴──┐  ┌──┴──────┐  ┌──────────────┐
│ Dim  │  │   Dim   │  │     Dim      │
│Doctor│  │ Patient │  │  Department  │
└──────┘  └─────────┘  └──────────────┘
```

---

## 🛠️ Tech Stack

| Tool | Usage |
|---|---|
| **PostgreSQL** | Data storage & Star Schema |
| **Power BI Desktop** | Dashboard & visualizations |
| **DAX** | Advanced measures with VAR/RETURN |
| **Python** | Data generation & preprocessing |
| **pandas / numpy** | Data simulation |

---

## 📁 Project Structure

```
healthcare-operations-intelligence/
│
├── data/
│   ├── Dim_Department.csv
│   ├── Dim_Doctor.csv
│   ├── Dim_Patient.csv
│   ├── Dim_Date.csv
│   ├── Fact_Admissions.csv
│   └── Fact_Billing.csv
│
├── sql/
│   └── healthcare_schema.sql
│
├── dashboard/
│   └── healthcare-operations-pro.pbix
│
├── screenshots/
│   ├── overview.png
│   ├── doctors.png
│   └── financial.png
│
└── README.md
```

---

## ⚙️ How to Run

### 1. Setup PostgreSQL

```bash
psql -U postgres -c "CREATE DATABASE healthcare_ops;"
```

### 2. Create Tables & Import Data

```bash
psql -U postgres -d healthcare_ops < healthcare_schema.sql

psql -U postgres -d healthcare_ops -c "\COPY dim_department FROM 'Dim_Department.csv' DELIMITER ',' CSV HEADER;"
psql -U postgres -d healthcare_ops -c "\COPY dim_doctor FROM 'Dim_Doctor.csv' DELIMITER ',' CSV HEADER;"
psql -U postgres -d healthcare_ops -c "\COPY dim_patient FROM 'Dim_Patient.csv' DELIMITER ',' CSV HEADER;"
psql -U postgres -d healthcare_ops -c "\COPY dim_date FROM 'Dim_Date.csv' DELIMITER ',' CSV HEADER;"
psql -U postgres -d healthcare_ops -c "\COPY fact_admissions FROM 'Fact_Admissions.csv' DELIMITER ',' CSV HEADER;"
psql -U postgres -d healthcare_ops -c "\COPY fact_billing FROM 'Fact_Billing.csv' DELIMITER ',' CSV HEADER;"
```

### 3. Open Power BI

- Open `healthcare-operations-pro.pbix`
- Update PostgreSQL connection: Server `localhost`, Database `healthcare_ops`

---

## 📊 DAX Measures

```dax
-- Total Admissions
Total Admissions = COUNTROWS('public fact_admissions')

-- Average Length of Stay
Avg Length of Stay =
VAR AvgLOS = AVERAGE('public fact_admissions'[los_days])
RETURN ROUND(AvgLOS, 1)

-- Average Wait Time
Avg Wait Time =
VAR AvgWait = AVERAGE('public fact_admissions'[waittime_min])
RETURN ROUND(AvgWait, 0)

-- Readmission Rate
Readmission Rate =
VAR TotalAdm = COUNTROWS('public fact_admissions')
VAR Readmitted = CALCULATE(
    COUNTROWS('public fact_admissions'),
    'public fact_admissions'[readmission_30d] = 1
)
RETURN DIVIDE(Readmitted, TotalAdm, 0)

-- Total Revenue
Total Revenue = SUM('public fact_billing'[totalbilled])

-- Average Satisfaction
Avg Satisfaction =
VAR AvgSat = AVERAGE('public fact_admissions'[satisfactionscore])
RETURN ROUND(AvgSat, 2)
```

---

## 🔐 Row-Level Security (RLS)

Dynamic RLS implemented to enforce data governance:

| Role | Access |
|---|---|
| **Department Manager** | Sees only their department's data |
| **CFO** | Full access to all departments |

```dax
-- Department Manager Filter
[DepartmentName] = USERPRINCIPALNAME()
```

---

## 📈 Dashboard Features

**Page 1 — Operations Overview:**
- 6 KPI Cards (Admissions, Revenue, Satisfaction, Readmission Rate, LOS, Wait Time)
- Admissions trend by month (chronological order)
- Admissions by department
- Readmission rate by department (with data labels)
- Avg satisfaction by department

**Page 2 — Doctor Performance:**
- Top 10 doctors by admissions
- Top 10 doctors by satisfaction score
- Top 10 doctors by wait time
- All with Top N filters and data labels

**Page 3 — Financial Overview:**
- Revenue by department (horizontal bar)
- Revenue trend by month (Jan → Dec)
- Payment status breakdown (Donut Chart with labels)
- 4 KPI Cards

**Navigation Bar** — Bookmark-based navigation between all 3 pages

---

## 📦 Dataset

- **Source:** Healthcare Operations Dataset
- **Size:** 10,500 admissions + 10,500 billing records
- **Patients:** 4,000 unique patients
- **Doctors:** 50 doctors across 8 departments
- **Period:** 4 years of data

---

## 💡 Business Recommendations

1. **Oncology** — Highest readmission rate (17.79%), needs care coordination review
2. **Emergency** — Lowest admissions but high wait times, capacity planning needed
3. **Cardiology** — Top revenue generator, invest in capacity expansion
4. **Pending payments** — 15.62% pending, implement automated billing follow-up
5. **Dr. Jackson** — Top performer with 428 admissions, benchmark his workflow

---

## 👤 Author

**Wagih Emad (Goose)**
BI Developer | Data Analyst
> *Building enterprise-grade data solutions for real business problems.*
