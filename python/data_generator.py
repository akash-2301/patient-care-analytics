import csv
import random
from datetime import datetime, timedelta
import os

# Create directories if they don't exist
os.makedirs('../data/raw', exist_ok=True)

# Helper functions
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def generate_data():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    first_names_m = ['Aarav', 'Vihaan', 'Aditya', 'Sai', 'Arjun', 'Kabir', 'Rahul', 'Rohan', 'Amit', 'Vikram', 'Ravi', 'Sanjay', 'Rajesh', 'Suresh', 'Karan']
    first_names_f = ['Aditi', 'Diya', 'Riya', 'Ananya', 'Kavya', 'Neha', 'Pooja', 'Priya', 'Anjali', 'Sneha', 'Meera', 'Ritu', 'Swati', 'Kiran', 'Nisha']
    last_names = ['Sharma', 'Singh', 'Patel', 'Kumar', 'Verma', 'Gupta', 'Reddy', 'Rao', 'Das', 'Joshi', 'Chauhan', 'Mishra', 'Pandey', 'Yadav', 'Tiwari']
    cities = ['Kanpur', 'Lucknow', 'Delhi', 'Mumbai', 'Varanasi', 'Agra', 'Pune', 'Bengaluru', 'Chennai', 'Hyderabad']
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    specializations = ['Cardiology', 'Dermatology', 'Orthopedics', 'Pediatrics', 'General Medicine', 'Neurology', 'ENT', 'Gynecology']
    treatment_types = {
        'Consultation': (500, 1500),
        'Surgery': (15000, 80000),
        'Therapy': (1000, 5000),
        'Lab Test': (300, 2000),
        'X-Ray': (500, 1500),
        'Blood Test': (200, 1000),
        'MRI': (3000, 8000),
        'Ultrasound': (800, 2500),
        'Vaccination': (500, 3000),
        'Follow-up': (300, 800)
    }

    # 1. Generate Patients (~300)
    patients = []
    num_patients = 300
    for i in range(1, num_patients + 1):
        gender = random.choice(['M', 'F'])
        first_name = random.choice(first_names_m) if gender == 'M' else random.choice(first_names_f)
        last_name = random.choice(last_names)
        age = random.randint(1, 90)
        phone = f"9{''.join([str(random.randint(0, 9)) for _ in range(9)])}"
        city = random.choice(cities)
        blood_group = random.choice(blood_groups)
        reg_date = random_date(start_date, datetime(2025, 1, 1)).strftime('%Y-%m-%d')
        patients.append([i, first_name, last_name, gender, age, phone, city, blood_group, reg_date])

    with open('../data/raw/patients.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['patient_id', 'first_name', 'last_name', 'gender', 'age', 'phone', 'address', 'blood_group', 'registration_date'])
        writer.writerows(patients)

    # 2. Generate Doctors (~30)
    doctors = []
    num_doctors = 30
    for i in range(1, num_doctors + 1):
        first_name = random.choice(first_names_m) # Keep it simple, just pick from m list for now
        last_name = random.choice(last_names)
        spec = random.choice(specializations)
        exp = random.randint(2, 30)
        phone = f"8{''.join([str(random.randint(0, 9)) for _ in range(9)])}"
        fee = random.choice([500, 800, 1000, 1200, 1500, 2000])
        doctors.append([i, first_name, last_name, spec, exp, phone, fee])
        
    with open('../data/raw/doctors.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['doctor_id', 'first_name', 'last_name', 'specialization', 'years_experience', 'phone', 'consultation_fee'])
        writer.writerows(doctors)

    # 3. Generate Appointments (~800)
    appointments = []
    num_appts = 800
    statuses = ['Completed']*60 + ['Cancelled']*15 + ['Scheduled']*15 + ['No-Show']*10
    
    for i in range(1, num_appts + 1):
        p_id = random.randint(1, num_patients)
        d_id = random.randint(1, num_doctors)
        # More likely on weekdays
        while True:
            appt_dt = random_date(start_date, datetime(2025, 10, 1))
            if appt_dt.weekday() < 5 or random.random() < 0.3:
                break
        
        appt_date = appt_dt.strftime('%Y-%m-%d')
        appt_time = f"{random.randint(9, 17):02d}:{random.choice(['00', '15', '30', '45'])}:00"
        status = random.choice(statuses)
        appointments.append([i, p_id, d_id, appt_date, appt_time, status])

    with open('../data/raw/appointments.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['appointment_id', 'patient_id', 'doctor_id', 'appointment_date', 'appointment_time', 'status'])
        writer.writerows(appointments)

    # 4. Generate Treatments (~500)
    # Only completed appointments should have treatments
    completed_appts = [a for a in appointments if a[5] == 'Completed']
    treatments = []
    num_treatments = min(500, len(completed_appts))
    
    # We'll just take the first 500 or so completed appointments
    selected_appts = random.sample(completed_appts, num_treatments)
    
    for i, appt in enumerate(selected_appts, 1):
        appt_id = appt[0]
        appt_date = appt[3]
        t_type = random.choice(list(treatment_types.keys()))
        min_cost, max_cost = treatment_types[t_type]
        cost = random.randint(min_cost, max_cost)
        # Treatment date is same or next day
        treat_dt = datetime.strptime(appt_date, '%Y-%m-%d') + timedelta(days=random.randint(0, 1))
        treatments.append([i, appt_id, t_type, treat_dt.strftime('%Y-%m-%d'), cost])

    with open('../data/raw/treatments.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['treatment_id', 'appointment_id', 'treatment_type', 'treatment_date', 'cost'])
        writer.writerows(treatments)

    # 5. Generate Billing (~500)
    billing = []
    pay_statuses = ['Paid']*70 + ['Pending']*15 + ['Insurance']*10 + ['Partially Paid']*5
    
    for i, t in enumerate(treatments, 1):
        t_id = t[0]
        appt_id = t[1]
        cost = t[4]
        # find patient_id from appt_id
        p_id = next(a[1] for a in appointments if a[0] == appt_id)
        
        discount = random.choice([0, 0, 0, 100, 200, 500]) if cost > 1000 else 0
        final_amount = max(0, cost - discount)
        pay_status = random.choice(pay_statuses)
        pay_date = t[3] if pay_status in ['Paid', 'Partially Paid'] else ''
        
        billing.append([i, p_id, t_id, cost, discount, final_amount, pay_status, pay_date])

    with open('../data/raw/billing.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['billing_id', 'patient_id', 'treatment_id', 'total_amount', 'discount', 'final_amount', 'payment_status', 'payment_date'])
        writer.writerows(billing)

if __name__ == '__main__':
    generate_data()
    print("Successfully generated all CSV files.")
