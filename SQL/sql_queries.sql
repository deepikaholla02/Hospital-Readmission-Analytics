USE healthcare_analytics;

select * from patient_data;

SELECT *
FROM patient_data
LIMIT 10;

-- Total Patients & Readmission Rate
SELECT
    COUNT(*) AS total_patients,
    SUM(readmitted) AS readmitted_patients,
    ROUND(SUM(readmitted) * 100.0 / COUNT(*), 2) AS readmission_rate_pct
FROM patient_data;

-- Average Hospital Stay by Specialty:
SELECT medical_specialty, AVG(time_in_hospital) AS avg_stay
FROM patient_data
GROUP BY medical_specialty
ORDER BY avg_stay DESC;

-- Readmission Rate by Medical Specialty
SELECT
    medical_specialty,
    COUNT(*) AS patients,
    ROUND(AVG(readmitted) * 100, 2) AS readmission_rate_pct
FROM patient_data
GROUP BY medical_specialty
ORDER BY readmission_rate_pct DESC;

-- Emergency Visits vs Readmission
SELECT
    n_emergency,
    COUNT(*) AS patients,
    ROUND(AVG(readmitted) * 100, 2) AS readmission_rate_pct
FROM patient_data
GROUP BY n_emergency
ORDER BY n_emergency;

-- Medication Load by Diagnosis
SELECT diag_1, AVG(n_medications) AS avg_meds
FROM patient_data
GROUP BY diag_1
ORDER BY avg_meds DESC
LIMIT 10;

-- Outpatient Visits vs. Readmission Risk
SELECT n_outpatient, AVG(readmitted) AS readmission_rate
FROM patient_data
GROUP BY n_outpatient
ORDER BY n_outpatient;

-- Readmission Rate by Age Bucket
SELECT age, AVG(readmitted) AS readmission_rate
FROM patient_data
GROUP BY age
ORDER BY age;

-- High-Risk Patient Identification
SELECT *
FROM patient_data
WHERE n_inpatient >= 2
  AND n_emergency >= 1
  AND n_medications >= 10
  AND readmitted = 1;