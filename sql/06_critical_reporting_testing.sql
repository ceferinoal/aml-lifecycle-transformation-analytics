/*
Project: AML Lifecycle Transformation Analytics
Module 06: Critical Reporting Testing

Objective:
Consolidate AML lifecycle exceptions into governance indicators for critical reporting.

Context:
AML Holding functions need reliable reporting to monitor customer lifecycle risks,
documentation gaps, restrictive measure gaps, geography rollout issues and training adoption.

This module simulates how SQL can support critical AML governance reporting by aggregating
exceptions across different lifecycle areas.
*/

-- ============================================================
-- Test 1: Customer risk rating inconsistencies by country
-- ============================================================

SELECT
    c.country,
    COUNT(*) AS rating_inconsistency_count
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
WHERE r.assigned_aml_rating IN ('LOW', 'MEDIUM')
  AND (
        f.pep_flag = 'YES'
        OR f.high_risk_country_flag = 'YES'
        OR f.complex_ownership_flag = 'YES'
        OR f.adverse_media_flag = 'YES'
        OR f.repeated_aml_issues_count >= 3
      )
GROUP BY c.country
ORDER BY rating_inconsistency_count DESC;


-- ============================================================
-- Test 2: Documentation gaps by AML rating
-- ============================================================

SELECT
    r.assigned_aml_rating,
    COUNT(*) AS documentation_gap_count
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE d.identity_document_status <> 'VALID'
   OR d.source_of_funds_status <> 'VALID'
   OR d.edd_file_status <> 'VALID'
   OR (
        c.customer_type = 'LEGAL_ENTITY'
        AND d.beneficial_ownership_status <> 'VALID'
      )
GROUP BY r.assigned_aml_rating
ORDER BY documentation_gap_count DESC;


-- ============================================================
-- Test 3: Restrictive measure gaps by country
-- ============================================================

SELECT
    c.country,
    COUNT(*) AS restrictive_measure_gap_count
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
LEFT JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE r.assigned_aml_rating IN ('HIGH', 'CRITICAL')
  AND (
        m.restrictive_measure_status IS NULL
        OR m.restrictive_measure_status = 'NOT_APPLIED'
        OR m.escalation_required_flag = 'NO'
      )
GROUP BY c.country
ORDER BY restrictive_measure_gap_count DESC;


-- ============================================================
-- Test 4: Geography rollout gaps by region
-- ============================================================

SELECT
    region,
    COUNT(*) AS rollout_gap_count,
    SUM(open_gaps_count) AS total_open_gaps
FROM geography_rollout
WHERE rollout_status <> 'IMPLEMENTED'
   OR open_gaps_count > 0
   OR remediation_status <> 'CLOSED'
GROUP BY region
ORDER BY total_open_gaps DESC;


-- ============================================================
-- Test 5: Training and communication gaps by business area
-- ============================================================

SELECT
    business_area,
    COUNT(*) AS training_communication_gap_count,
    AVG(completion_rate) AS average_completion_rate
FROM training_communications
WHERE training_status <> 'COMPLETED'
   OR completion_rate < 0.80
   OR acknowledgement_status <> 'ACKNOWLEDGED'
GROUP BY business_area
ORDER BY training_communication_gap_count DESC;


-- ============================================================
-- Test 6: Critical reports overdue or not submitted
-- ============================================================

SELECT
    report_id,
    report_name,
    reporting_area,
    report_owner,
    reporting_frequency,
    due_date,
    submission_status,
    escalation_status
FROM critical_reports
WHERE submission_status <> 'SUBMITTED'
  AND due_date < CURRENT_DATE;


-- ============================================================
-- Test 7: Critical report items open without escalation
-- ============================================================

SELECT
    report_id,
    report_name,
    reporting_area,
    report_owner,
    open_issues_count,
    high_severity_issues_count,
    escalation_status
FROM critical_reports
WHERE high_severity_issues_count > 0
  AND escalation_status <> 'ESCALATED';


-- ============================================================
-- Test 8: Executive AML lifecycle KRI summary
-- ============================================================

SELECT
    'Customer Risk Rating' AS reporting_area,
    COUNT(*) AS exception_count
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
WHERE r.assigned_aml_rating IN ('LOW', 'MEDIUM')
  AND (
        f.pep_flag = 'YES'
        OR f.high_risk_country_flag = 'YES'
        OR f.complex_ownership_flag = 'YES'
        OR f.adverse_media_flag = 'YES'
        OR f.repeated_aml_issues_count >= 3
      )

UNION ALL

SELECT
    'Documentation Standards' AS reporting_area,
    COUNT(*) AS exception_count
FROM customers c
JOIN customer_documents d
    ON c.customer_id = d.customer_id
WHERE d.identity_document_status <> 'VALID'
   OR d.source_of_funds_status <> 'VALID'
   OR d.edd_file_status <> 'VALID'
   OR (
        c.customer_type = 'LEGAL_ENTITY'
        AND d.beneficial_ownership_status <> 'VALID'
      )

UNION ALL

SELECT
    'Restrictive Measures' AS reporting_area,
    COUNT(*) AS exception_count
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
LEFT JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE r.assigned_aml_rating IN ('HIGH', 'CRITICAL')
  AND (
        m.restrictive_measure_status IS NULL
        OR m.restrictive_measure_status = 'NOT_APPLIED'
        OR m.escalation_required_flag = 'NO'
      )

UNION ALL

SELECT
    'Geography Rollout' AS reporting_area,
    COUNT(*) AS exception_count
FROM geography_rollout
WHERE rollout_status <> 'IMPLEMENTED'
   OR open_gaps_count > 0
   OR remediation_status <> 'CLOSED'

UNION ALL

SELECT
    'Training & Communication' AS reporting_area,
    COUNT(*) AS exception_count
FROM training_communications
WHERE training_status <> 'COMPLETED'
   OR completion_rate < 0.80
   OR acknowledgement_status <> 'ACKNOWLEDGED'

UNION ALL

SELECT
    'Critical Reporting' AS reporting_area,
    COUNT(*) AS exception_count
FROM critical_reports
WHERE submission_status <> 'SUBMITTED'
   OR high_severity_issues_count > 0;