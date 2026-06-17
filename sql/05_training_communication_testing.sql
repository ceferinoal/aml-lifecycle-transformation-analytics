/*
Project: AML Lifecycle Transformation Analytics
Module 05: Training & Communication Testing

Objective:
Identify potential gaps in AML lifecycle training, communication and customer knowledge culture across areas and geographies.

Context:
AML Lifecycle Transformation requires that corporate AML standards are not only defined,
but also understood and applied by the relevant teams.

Training, communication and culture are essential to ensure that Business, Compliance,
Risk, Engineering and Operations understand customer knowledge requirements and apply
the risk-based approach consistently.
*/

-- ============================================================
-- Test 1: Critical areas without AML lifecycle training completed
-- ============================================================

SELECT
    training_id,
    country,
    region,
    business_area,
    target_population,
    training_name,
    training_status,
    completion_rate,
    training_deadline
FROM training_communications
WHERE critical_area_flag = 'YES'
  AND training_status <> 'COMPLETED';


-- ============================================================
-- Test 2: Training deadline missed
-- ============================================================

SELECT
    training_id,
    country,
    region,
    business_area,
    training_name,
    training_status,
    completion_rate,
    training_deadline
FROM training_communications
WHERE training_status <> 'COMPLETED'
  AND training_deadline < CURRENT_DATE;


-- ============================================================
-- Test 3: Low completion rate in AML lifecycle training
-- ============================================================

SELECT
    training_id,
    country,
    region,
    business_area,
    training_name,
    target_population,
    completion_rate,
    training_status
FROM training_communications
WHERE completion_rate < 0.80;


-- ============================================================
-- Test 4: Communication sent but not acknowledged by target area
-- ============================================================

SELECT
    communication_id,
    country,
    region,
    business_area,
    communication_topic,
    communication_date,
    acknowledgement_status,
    acknowledgement_due_date
FROM training_communications
WHERE communication_date IS NOT NULL
  AND acknowledgement_status <> 'ACKNOWLEDGED';


-- ============================================================
-- Test 5: Acknowledgement deadline missed
-- ============================================================

SELECT
    communication_id,
    country,
    region,
    business_area,
    communication_topic,
    acknowledgement_status,
    acknowledgement_due_date
FROM training_communications
WHERE acknowledgement_status <> 'ACKNOWLEDGED'
  AND acknowledgement_due_date < CURRENT_DATE;


-- ============================================================
-- Test 6: Areas involved in onboarding without updated KYC training
-- ============================================================

SELECT
    training_id,
    country,
    region,
    business_area,
    onboarding_involved_flag,
    training_name,
    last_training_completion_date,
    training_status
FROM training_communications
WHERE onboarding_involved_flag = 'YES'
  AND (
        last_training_completion_date IS NULL
        OR last_training_completion_date < CURRENT_DATE - INTERVAL '12 months'
      );