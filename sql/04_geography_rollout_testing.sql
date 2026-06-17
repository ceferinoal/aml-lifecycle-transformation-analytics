/*
Project: AML Lifecycle Transformation Analytics
Module 04: Geography Rollout Testing

Objective:
Identify potential gaps in the rollout of corporate AML lifecycle standards across geographies.

Context:
AML Holding functions are responsible for defining corporate standards and ensuring that
those standards are communicated, deployed and monitored across different countries,
business areas and stakeholders.

This module focuses on governance, traceability, ownership, deadlines and remediation.
*/

-- ============================================================
-- Test 1: Geographies where AML lifecycle standard has not been implemented
-- ============================================================

SELECT
    geography_id,
    country,
    region,
    aml_standard_name,
    corporate_standard_version,
    rollout_status,
    implementation_deadline,
    actual_implementation_date
FROM geography_rollout
WHERE rollout_status <> 'IMPLEMENTED';


-- ============================================================
-- Test 2: Rollout implementation deadline missed
-- ============================================================

SELECT
    geography_id,
    country,
    region,
    aml_standard_name,
    corporate_standard_version,
    rollout_status,
    implementation_deadline,
    actual_implementation_date
FROM geography_rollout
WHERE rollout_status <> 'IMPLEMENTED'
  AND implementation_deadline < CURRENT_DATE;


-- ============================================================
-- Test 3: Corporate standard communicated but not implemented
-- ============================================================

SELECT
    geography_id,
    country,
    region,
    aml_standard_name,
    corporate_standard_version,
    communication_date,
    rollout_status,
    implementation_deadline
FROM geography_rollout
WHERE communication_date IS NOT NULL
  AND rollout_status IN ('NOT_STARTED', 'IN_PROGRESS', 'DELAYED');


-- ============================================================
-- Test 4: Geographies without local owner assigned
-- ============================================================

SELECT
    geography_id,
    country,
    region,
    aml_standard_name,
    rollout_status,
    local_owner,
    local_owner_assigned_flag
FROM geography_rollout
WHERE local_owner_assigned_flag = 'NO'
   OR local_owner IS NULL;


-- ============================================================
-- Test 5: Geographies with open rollout gaps and overdue remediation
-- ============================================================

SELECT
    geography_id,
    country,
    region,
    aml_standard_name,
    rollout_status,
    open_gaps_count,
    remediation_due_date,
    remediation_status
FROM geography_rollout
WHERE open_gaps_count > 0
  AND remediation_due_date < CURRENT_DATE
  AND remediation_status <> 'CLOSED';


-- ============================================================
-- Test 6: Implemented geographies with unresolved post-implementation gaps
-- ============================================================

SELECT
    geography_id,
    country,
    region,
    aml_standard_name,
    rollout_status,
    actual_implementation_date,
    open_gaps_count,
    remediation_status
FROM geography_rollout
WHERE rollout_status = 'IMPLEMENTED'
  AND open_gaps_count > 0
  AND remediation_status <> 'CLOSED';