import pandas as pd
import numpy as np
from datetime import date, timedelta
import random

np.random.seed(42)
random.seed(42)

# ============================================
# Dim_Department
# ============================================
departments = pd.DataFrame({
    'department_id': range(1, 9),
    'department_name': ['Emergency', 'Surgery', 'Cardiology', 
                       'Orthopedics', 'Pediatrics', 'Oncology', 
                       'Neurology', 'ICU'],
    'total_beds': [50, 30, 40, 35, 45, 25, 30, 20],
    'cost_per_day': [800, 1200, 1000, 950, 700, 1500, 1100, 2000]
})

# ============================================
# Dim_Doctor
# ============================================
first_names = ['Ahmed', 'Mohamed', 'Sara', 'Nour', 'Khaled', 
               'Mona', 'Omar', 'Heba', 'Tarek', 'Dina']
last_names = ['Hassan', 'Ibrahim', 'Ali', 'Mahmoud', 'Salem',
              'Youssef', 'Farouk', 'Nasser', 'Kamel', 'Zaki']
specializations = {
    1: 'Emergency Medicine', 2: 'General Surgery',
    3: 'Cardiology', 4: 'Orthopedic Surgery',
    5: 'Pediatrics', 6: 'Oncology',
    7: 'Neurology', 8: 'Critical Care'
}

doctors = []
doctor_id = 1
for dept_id in range(1, 9):
    num_doctors = random.randint(5, 8)
    for _ in range(num_doctors):
        doctors.append({
            'doctor_id': doctor_id,
            'doctor_name': f"Dr. {random.choice(first_names)} {random.choice(last_names)}",
            'department_id': dept_id,
            'specialization': specializations[dept_id],
            'years_experience': random.randint(3, 25),
            'rating': round(random.uniform(3.5, 5.0), 1)
        })
        doctor_id += 1

dim_doctor = pd.DataFrame(doctors)

# ============================================
# Dim_Patient
# ============================================
patients = []
for i in range(1, 5001):
    age = random.randint(1, 90)
    patients.append({
        'patient_id': i,
        'patient_name': f"Patient_{i:04d}",
        'age': age,
        'age_group': 'Child' if age < 18 else ('Adult' if age < 60 else 'Senior'),
        'gender': random.choice(['Male', 'Female']),
        'city': random.choice(['Cairo', 'Alexandria', 'Giza', 'Luxor', 
                               'Aswan', 'Mansoura', 'Tanta', 'Suez']),
        'insurance_type': random.choice(['Private', 'Government', 'Self-Pay', 'Corporate'])
    })

dim_patient = pd.DataFrame(patients)

# ============================================
# Dim_Date
# ============================================
dates = pd.date_range(start='2021-01-01', end='2024-12-31', freq='D')
dim_date = pd.DataFrame({
    'date': dates,
    'year': dates.year,
    'month': dates.month,
    'month_name': dates.strftime('%B'),
    'quarter': dates.quarter,
    'day_of_week': dates.strftime('%A'),
    'is_weekend': dates.dayofweek >= 5
})

# ============================================
# Fact_Admissions
# ============================================
admissions = []
admission_id = 1

for year in range(2021, 2025):
    for month in range(1, 13):
        for dept_id in range(1, 9):
            dept = departments[departments['department_id'] == dept_id].iloc[0]
            
            # حجم الـ admissions بيتغير حسب القسم والموسم
            base_admissions = {
                1: 120, 2: 60, 3: 80, 4: 70,
                5: 90, 6: 50, 7: 60, 8: 40
            }[dept_id]
            
            seasonality = 1 + 0.2 * np.sin((month - 1) * np.pi / 6)
            growth = 1 + (year - 2021) * 0.05
            num_admissions = int(base_admissions * seasonality * growth * 
                               np.random.uniform(0.85, 1.15))
            
            dept_doctors = dim_doctor[dim_doctor['department_id'] == dept_id]['doctor_id'].tolist()
            
            for _ in range(num_admissions):
                admission_date = date(year, month, random.randint(1, 28))
                los = max(1, int(np.random.exponential(
                    {'Emergency': 2, 'Surgery': 7, 'Cardiology': 5,
                     'Orthopedics': 6, 'Pediatrics': 3, 'Oncology': 10,
                     'Neurology': 6, 'ICU': 8}[dept['department_name']]
                )))
                
                wait_time = max(5, int(np.random.normal(
                    {'Emergency': 45, 'Surgery': 120, 'Cardiology': 90,
                     'Orthopedics': 100, 'Pediatrics': 60, 'Oncology': 150,
                     'Neurology': 110, 'ICU': 30}[dept['department_name']], 20
                )))
                
                admission_type = random.choices(
                    ['Emergency', 'Elective', 'Urgent'],
                    weights=[0.3, 0.5, 0.2]
                )[0]
                
                outcome = random.choices(
                    ['Discharged', 'Transferred', 'Deceased', 'Against Advice'],
                    weights=[0.85, 0.08, 0.05, 0.02]
                )[0]
                
                readmitted = 1 if (outcome == 'Discharged' and 
                                  random.random() < 0.08) else 0
                
                satisfaction = round(random.uniform(
                    3.0 if wait_time > 120 else 3.5, 5.0
                ), 1)

                admissions.append({
                    'admission_id': admission_id,
                    'patient_id': random.randint(1, 5000),
                    'doctor_id': random.choice(dept_doctors),
                    'department_id': dept_id,
                    'admission_date': admission_date,
                    'length_of_stay': los,
                    'wait_time_minutes': wait_time,
                    'admission_type': admission_type,
                    'outcome': outcome,
                    'readmitted_30days': readmitted,
                    'satisfaction_score': satisfaction
                })
                admission_id += 1

fact_admissions = pd.DataFrame(admissions)

# ============================================
# Fact_Billing
# ============================================
billing = []
for _, adm in fact_admissions.iterrows():
    dept = departments[departments['department_id'] == adm['department_id']].iloc[0]
    
    base_cost = dept['cost_per_day'] * adm['length_of_stay']
    medication_cost = round(base_cost * random.uniform(0.15, 0.35), 2)
    lab_cost = round(base_cost * random.uniform(0.10, 0.20), 2)
    total_cost = round(base_cost + medication_cost + lab_cost, 2)
    
    insurance_coverage = {
        'Private': 0.80, 'Government': 0.70,
        'Corporate': 0.90, 'Self-Pay': 0.0
    }
    
    patient = dim_patient[dim_patient['patient_id'] == adm['patient_id']].iloc[0]
    coverage = insurance_coverage[patient['insurance_type']]
    insurance_paid = round(total_cost * coverage, 2)
    patient_paid = round(total_cost - insurance_paid, 2)
    
    billing.append({
        'billing_id': adm['admission_id'],
        'admission_id': adm['admission_id'],
        'total_cost': total_cost,
        'medication_cost': medication_cost,
        'lab_cost': lab_cost,
        'insurance_paid': insurance_paid,
        'patient_paid': patient_paid,
        'payment_status': random.choices(
            ['Paid', 'Pending', 'Partial', 'Waived'],
            weights=[0.70, 0.15, 0.10, 0.05]
        )[0]
    })

fact_billing = pd.DataFrame(billing)

# ============================================
# Export
# ============================================
path = '/Users/wagihemadwagih/Downloads/'
departments.to_csv(f'{path}dim_department.csv', index=False)
dim_doctor.to_csv(f'{path}dim_doctor.csv', index=False)
dim_patient.to_csv(f'{path}dim_patient.csv', index=False)
dim_date.to_csv(f'{path}dim_date.csv', index=False)
fact_admissions.to_csv(f'{path}fact_admissions.csv', index=False)
fact_billing.to_csv(f'{path}fact_billing.csv', index=False)

print("✅ dim_department:", len(departments), "rows")
print("✅ dim_doctor:", len(dim_doctor), "rows")
print("✅ dim_patient:", len(dim_patient), "rows")
print("✅ dim_date:", len(dim_date), "rows")
print("✅ fact_admissions:", len(fact_admissions), "rows")
print("✅ fact_billing:", len(fact_billing), "rows")
print("\n🎉 Healthcare data generated!")