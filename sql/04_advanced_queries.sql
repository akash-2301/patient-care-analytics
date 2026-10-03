-- ==============================================================================
-- Portfolio Project: Patient Care Analytics
-- File: 04_advanced_queries.sql
-- Description: Advanced queries using CTEs, Window Functions, and Subqueries.
-- Kept these interview-friendly to show analytical thinking.
-- ==============================================================================

USE hospital_db;

-- Q1: CTE: Monthly revenue trend
WITH MonthlyRevenue AS (
    SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month, SUM(final_amount) AS revenue
    FROM billing
    WHERE payment_status IN ('Paid', 'Partially Paid')
    GROUP BY month
)
SELECT * FROM MonthlyRevenue
ORDER BY month;
-- Used a CTE to make the query more readable before selecting from it.
-- Insight: Tracks financial performance over time.

-- Q2: CTE: Patient visit frequency classification
WITH PatientVisits AS (
    SELECT patient_id, COUNT(*) AS visit_count
    FROM appointments
    GROUP BY patient_id
)
SELECT 
    CASE 
        WHEN visit_count = 1 THEN 'One-time'
        WHEN visit_count BETWEEN 2 AND 4 THEN 'Regular'
        ELSE 'Frequent' 
    END AS patient_type,
    COUNT(*) AS num_patients
FROM PatientVisits
GROUP BY patient_type;
-- Insight: Shows patient retention. Too many 'One-time' means low retention.

-- Q3: Window Function RANK: Top 3 doctors by revenue
WITH DoctorRevenue AS (
    SELECT d.doctor_id, d.first_name, d.last_name, SUM(b.final_amount) AS total_revenue
    FROM doctors d
    JOIN appointments a ON d.doctor_id = a.doctor_id
    JOIN treatments t ON a.appointment_id = t.appointment_id
    JOIN billing b ON t.treatment_id = b.treatment_id
    GROUP BY d.doctor_id, d.first_name, d.last_name
)
SELECT first_name, last_name, total_revenue,
       RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM DoctorRevenue
LIMIT 3;
-- Used RANK() window function to find top performers.
-- Insight: Reward top-performing doctors with bonuses.

-- Q4: Window Function DENSE_RANK: Top patients by spend
WITH PatientSpend AS (
    SELECT p.patient_id, p.first_name, p.last_name, SUM(b.final_amount) AS total_spent
    FROM patients p
    JOIN billing b ON p.patient_id = b.patient_id
    GROUP BY p.patient_id, p.first_name, p.last_name
)
SELECT first_name, last_name, total_spent,
       DENSE_RANK() OVER (ORDER BY total_spent DESC) AS spend_rank
FROM PatientSpend
LIMIT 5;
-- Used DENSE_RANK() so there are no gaps in ranking if there are ties.
-- Insight: Identify priority patients for relationship management.

-- Q5: Running total of revenue by month
WITH MonthlyStats AS (
    SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month, SUM(final_amount) AS monthly_revenue
    FROM billing
    WHERE payment_status = 'Paid' AND payment_date IS NOT NULL
    GROUP BY month
)
SELECT month, monthly_revenue,
       SUM(monthly_revenue) OVER (ORDER BY month) AS running_total
FROM MonthlyStats;
-- Window functions for running totals show cumulative growth easily.
-- Insight: Visualizing cumulative revenue helps in checking yearly targets.

-- Q6: Subquery: Patients with above-average bills
SELECT b.billing_id, b.patient_id, b.final_amount
FROM billing b
WHERE b.final_amount > (SELECT AVG(final_amount) FROM billing);
-- Used a subquery in the WHERE clause to filter based on an aggregate.
-- Insight: Investigating unusually high bills for auditing purposes.

-- Q7: Subquery: Doctors earning more than average
SELECT d.first_name, d.last_name, d.consultation_fee
FROM doctors d
WHERE d.consultation_fee > (SELECT AVG(consultation_fee) FROM doctors);
-- Insight: Reviews if senior doctors justify their higher fees compared to the average.

-- Q8: HAVING: Treatment types with average cost > 5000
SELECT treatment_type, AVG(cost) AS avg_cost
FROM treatments
GROUP BY treatment_type
HAVING AVG(cost) > 5000;
-- Practicing HAVING clause to filter groups after GROUP BY.
-- Insight: Isolates the most expensive procedures for cost-reduction analysis.

-- Q9: Cohort-style: Patient retention (patients who came back for 2+ appointments)
SELECT patient_id, COUNT(appointment_id) AS total_visits
FROM appointments
GROUP BY patient_id
HAVING COUNT(appointment_id) >= 2;
-- Insight: These are loyal patients; tracking this number over time measures hospital reputation.

-- Q10: Year-over-year comparison of appointments
SELECT 
    YEAR(appointment_date) AS year, 
    COUNT(*) AS total_appointments
FROM appointments
GROUP BY YEAR(appointment_date)
ORDER BY year;
-- Simple extraction of YEAR to do high-level trend analysis.
-- Insight: Management uses this to report annual growth to stakeholders.
