-- ==============================================================================
-- Portfolio Project: Patient Care Analytics
-- File: 03_intermediate_queries.sql
-- Description: Queries involving JOINs, more complex groupings, and business logic.
-- I focused on connecting tables to answer real business questions.
-- ==============================================================================

USE hospital_db;

-- Q1: Who are the most active patients? (Most appointments)
SELECT p.first_name, p.last_name, COUNT(a.appointment_id) AS visit_count
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY visit_count DESC
LIMIT 10;
-- Joined patients and appointments.
-- Insight: Recognizing frequent visitors can help in creating loyalty or chronic care programs.

-- Q2: Who are the busiest doctors?
SELECT d.first_name, d.last_name, d.specialization, COUNT(a.appointment_id) AS appointment_count
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
ORDER BY appointment_count DESC
LIMIT 5;
-- Insight: Busiest doctors might be overworked; hospital might need to hire more staff in their specialization.

-- Q3: How much revenue was generated per doctor?
SELECT d.first_name, d.last_name, SUM(b.final_amount) AS total_revenue
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
JOIN treatments t ON a.appointment_id = t.appointment_id
JOIN billing b ON t.treatment_id = b.treatment_id
GROUP BY d.doctor_id, d.first_name, d.last_name
ORDER BY total_revenue DESC;
-- Practiced joining 4 tables together to trace data from doctor to payment.
-- Insight: Identifying high-revenue doctors helps in performance evaluations.

-- Q4: What is the average bill amount per treatment type?
SELECT t.treatment_type, ROUND(AVG(b.final_amount), 2) AS avg_bill
FROM treatments t
JOIN billing b ON t.treatment_id = b.treatment_id
GROUP BY t.treatment_type
ORDER BY avg_bill DESC;
-- Insight: Shows which procedures are the most lucrative for the hospital.

-- Q5: Month-over-month appointment growth
SELECT 
    DATE_FORMAT(appointment_date, '%Y-%m') AS month,
    COUNT(appointment_id) AS total_appointments
FROM appointments
GROUP BY month
ORDER BY month;
-- Insight: Helps management see if the patient volume is increasing or decreasing over time.

-- Q6: What is the no-show rate by doctor?
SELECT d.first_name, d.last_name,
       SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) AS no_shows,
       COUNT(a.appointment_id) AS total_appointments,
       ROUND((SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) / COUNT(a.appointment_id)) * 100, 2) AS no_show_rate
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name
ORDER BY no_show_rate DESC;
-- Used conditional aggregation with CASE inside SUM.
-- Insight: High no-show rates for specific doctors might indicate issues with scheduling or patient satisfaction.

-- Q7: Who are the top 5 highest-paying patients?
SELECT p.first_name, p.last_name, SUM(b.final_amount) AS total_spent
FROM patients p
JOIN billing b ON p.patient_id = b.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name
ORDER BY total_spent DESC
LIMIT 5;
-- Insight: Premium patients could be offered VIP healthcare packages.

-- Q8: Which day of the week gets the most appointments?
-- I wanted to find which day gets the most patients so the hospital can plan staffing.
SELECT DAYNAME(appointment_date) AS day_of_week, COUNT(*) AS appointment_count
FROM appointments
GROUP BY day_of_week
ORDER BY appointment_count DESC;
-- Used DAYNAME to extract the weekday from the date.
-- Insight: If Mondays are busiest, the hospital should schedule more staff on Mondays.

-- Q9: Is there a difference in average treatment cost by gender?
SELECT p.gender, ROUND(AVG(t.cost), 2) AS avg_treatment_cost
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
JOIN treatments t ON a.appointment_id = t.appointment_id
GROUP BY p.gender;
-- Insight: Could reveal if certain demographic groups require more expensive procedures.

-- Q10: Are there any patients who registered but never booked an appointment?
SELECT p.first_name, p.last_name, p.phone
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
WHERE a.appointment_id IS NULL;
-- Used LEFT JOIN to find non-matching records.
-- Insight: The marketing team can call these patients and offer a free first consultation.

-- Q11: Are there any doctors with zero appointments?
SELECT d.first_name, d.last_name, d.specialization
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
WHERE a.appointment_id IS NULL;
-- Insight: Helps identify new hires who need marketing or doctors on leave.

-- Q12: Patient age segmentation using CASE WHEN
SELECT 
    CASE 
        WHEN age < 18 THEN 'Pediatric'
        WHEN age BETWEEN 18 AND 60 THEN 'Adult'
        ELSE 'Senior' 
    END AS life_stage,
    COUNT(*) AS count
FROM patients
GROUP BY life_stage;
-- Insight: Adjusts hospital facilities (like waiting rooms) based on major demographics.

-- Q13: Categorizing revenue into buckets using CASE WHEN
SELECT b.billing_id, b.final_amount,
    CASE 
        WHEN b.final_amount < 1000 THEN 'Low Value'
        WHEN b.final_amount BETWEEN 1000 AND 10000 THEN 'Medium Value'
        ELSE 'High Value'
    END AS revenue_bucket
FROM billing b;
-- Insight: Helps finance team analyze the spread of small vs large bills.

-- Q14: What is the appointment conversion rate? (Completed vs Scheduled)
SELECT 
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_count,
    COUNT(*) AS total_appointments,
    ROUND((SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS conversion_rate
FROM appointments;
-- Insight: A low completion rate means the hospital is losing potential revenue.

-- Q15: Which city brings in the most revenue?
SELECT p.address AS city, SUM(b.final_amount) AS total_revenue
FROM patients p
JOIN billing b ON p.patient_id = b.patient_id
GROUP BY p.address
ORDER BY total_revenue DESC;
-- Insight: Helps focus regional advertising budgets on the most profitable cities.
