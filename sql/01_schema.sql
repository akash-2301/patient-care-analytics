-- ==============================================================================
-- Portfolio Project: Patient Care Analytics
-- File: 01_schema.sql
-- Description: Creates the database and tables for the hospital data.
-- I am setting up primary and foreign keys to ensure data integrity.
-- ==============================================================================

-- Create the database
CREATE DATABASE IF NOT EXISTS hospital_db;

-- Use the database
USE hospital_db;

-- ==============================================================================
-- 1. Patients Table
-- Stores all patient demographic details. 
-- patient_id is the primary key.
-- ==============================================================================
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender CHAR(1), -- 'M' or 'F'
    age INT,
    phone VARCHAR(15),
    address VARCHAR(100),
    blood_group VARCHAR(5),
    registration_date DATE
);

-- ==============================================================================
-- 2. Doctors Table
-- Stores doctor profiles including their specialization and fees.
-- ==============================================================================
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(50),
    years_experience INT,
    phone VARCHAR(15),
    consultation_fee DECIMAL(10, 2)
);

-- ==============================================================================
-- 3. Appointments Table
-- Links patients and doctors for scheduled visits.
-- Has foreign keys pointing to patients and doctors.
-- ==============================================================================
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(20), -- e.g., 'Completed', 'Cancelled', 'Scheduled', 'No-Show'
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- ==============================================================================
-- 4. Treatments Table
-- Details the medical procedures or tests done during an appointment.
-- ==============================================================================
CREATE TABLE treatments (
    treatment_id INT PRIMARY KEY,
    appointment_id INT,
    treatment_type VARCHAR(50),
    treatment_date DATE,
    cost DECIMAL(10, 2),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

-- ==============================================================================
-- 5. Billing Table
-- Tracks payments for treatments. Links to both patient and treatment.
-- ==============================================================================
CREATE TABLE billing (
    billing_id INT PRIMARY KEY,
    patient_id INT,
    treatment_id INT,
    total_amount DECIMAL(10, 2),
    discount DECIMAL(10, 2),
    final_amount DECIMAL(10, 2),
    payment_status VARCHAR(20), -- e.g., 'Paid', 'Pending', 'Insurance', 'Partially Paid'
    payment_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id)
);
