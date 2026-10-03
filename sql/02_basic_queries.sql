-- ==============================================================================
-- Portfolio Project: Patient Care Analytics
-- File: 02_basic_queries.sql
-- Description: Simple queries to understand the data distribution.
-- I wrote these to show basic SELECT, filtering, and aggregation skills.
-- ==============================================================================

USE hospital_db;

-- Q1: What is the total number of patients?
SELECT COUNT(*) AS total_patients 
FROM patients;
-- This uses COUNT to give a single number.
-- Insight: 300 patients registered over 2 years shows steady growth.

-- Q2: What is the total number of doctors?
SELECT COUNT(*) AS total_doctors 
FROM doctors;
-- Simple COUNT on the doctors table.
-- Insight: 30 doctors on staff, which helps handle the 300 patients effectively.

-- Q3: What is the total number of appointments scheduled?
SELECT COUNT(*) AS total_appointments 
FROM appointments;
-- Insight: 800 appointments means patients visit multiple times on average.

-- Q4: What is the gender distribution of our patients?
SELECT gender, COUNT(*) AS patient_count
FROM patients
GROUP BY gender;
-- This uses GROUP BY + COUNT which I practiced to understand data aggregation.
-- Insight: Helps the hospital know if they need to focus more on men's or women's health.

-- Q5: How are patients distributed across age groups?
-- I am using CASE WHEN to create custom age buckets.
SELECT 
    CASE 
        WHEN age BETWEEN 0 AND 18 THEN '0-18'
        WHEN age BETWEEN 19 AND 35 THEN '19-35'
        WHEN age BETWEEN 36 AND 50 THEN '36-50'
        ELSE '51+' 
    END AS age_group,
    COUNT(*) AS patient_count
FROM patients
GROUP BY age_group
ORDER BY patient_count DESC;
-- Used CASE for conditional logic in SQL.
-- Insight: Identifying the most common age group helps in planning relevant specializations.

-- Q6: Which are the top 5 cities by patient count?
SELECT address AS city, COUNT(*) AS patient_count
FROM patients
GROUP BY address
ORDER BY patient_count DESC
LIMIT 5;
-- ORDER BY DESC and LIMIT helps find the top values.
-- Insight: The hospital might want to open clinics in the top cities.

-- Q7: What is the distribution of blood groups among patients?
SELECT blood_group, COUNT(*) AS count
FROM patients
GROUP BY blood_group
ORDER BY count DESC;
-- Insight: Useful for the blood bank to know which blood types are most commonly needed.

-- Q8: Who are the most experienced doctors on staff?
SELECT first_name, last_name, specialization, years_experience
FROM doctors
ORDER BY years_experience DESC;
-- Sorting by experience to see senior staff.
-- Insight: Promoting highly experienced doctors can build trust with patients.

-- Q9: How many doctors do we have per specialization?
SELECT specialization, COUNT(*) AS doctor_count
FROM doctors
GROUP BY specialization
ORDER BY doctor_count DESC;
-- Insight: Shows if the hospital is short-staffed in critical areas like Cardiology.

-- Q10: What is the distribution of appointment statuses?
SELECT status, COUNT(*) AS status_count
FROM appointments
GROUP BY status;
-- Insight: High 'No-Show' or 'Cancelled' rates could indicate scheduling issues.

-- Q11: How many appointments were there each month?
SELECT 
    DATE_FORMAT(appointment_date, '%Y-%m') AS appointment_month,
    COUNT(*) AS total_appointments
FROM appointments
GROUP BY appointment_month
ORDER BY appointment_month;
-- Using date formatting to group by month.
-- Insight: Helps identify seasonal trends in hospital visits.

-- Q12: What were the recent appointments in the last 30 days?
-- (Assuming current date is 2025-10-01 for this example)
SELECT *
FROM appointments
WHERE appointment_date >= '2025-09-01'
ORDER BY appointment_date DESC;
-- Filtering dates using WHERE.
-- Insight: Tracking recent activity is crucial for daily operations.

-- Q13: What is the distribution of different treatment types?
SELECT treatment_type, COUNT(*) AS count
FROM treatments
GROUP BY treatment_type
ORDER BY count DESC;
-- Insight: Knowing the most common treatments helps in inventory and lab planning.

-- Q14: What are the min, max, and average costs of treatments?
SELECT 
    MIN(cost) AS min_cost, 
    MAX(cost) AS max_cost, 
    ROUND(AVG(cost), 2) AS avg_cost
FROM treatments;
-- Practicing aggregate functions like MIN, MAX, and AVG.
-- Insight: Gives a quick overview of the hospital's pricing spectrum.

-- Q15: What is the breakdown of payment statuses?
SELECT payment_status, COUNT(*) AS count
FROM billing
GROUP BY payment_status;
-- Insight: A high number of 'Pending' statuses means the collection team needs to follow up.
