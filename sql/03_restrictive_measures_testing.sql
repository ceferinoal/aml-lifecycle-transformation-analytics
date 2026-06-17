/*
Project: AML Lifecycle Transformation Analytics
Module 03: Restrictive Measures Testing

Objective:
Identify potential gaps between customer AML risk profile and the restrictive or enhanced measures applied.

Context:
AML Lifecycle Transformation requires that customer risk is translated into appropriate actions.
For higher-risk customers, this may include enhanced monitoring, documentation restrictions,
onboarding limitations, transactional restrictions or escalation requirements.
*/

-- ============================================================
-- Test 1: HIGH risk customers without any restrictive measure
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    m.restrictive_measure_status,
    m.measure_type
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
LEFT JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE r.assigned_aml_rating = 'HIGH'
  AND (
        m.restrictive_measure_status IS NULL
        OR m.restrictive_measure_status = 'NOT_APPLIED'
      );


-- ============================================================
-- Test 2: Customers with adverse media but no enhanced monitoring
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    f.adverse_media_flag,
    m.enhanced_monitoring_flag
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
LEFT JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE f.adverse_media_flag = 'YES'
  AND (
        m.enhanced_monitoring_flag IS NULL
        OR m.enhanced_monitoring_flag = 'NO'
      );


-- ============================================================
-- Test 3: Customers with incomplete documentation but no onboarding restriction
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    c.customer_status,
    r.assigned_aml_rating,
    d.identity_document_status,
    d.source_of_funds_status,
    d.beneficial_ownership_status,
    d.edd_file_status,
    m.onboarding_restriction_flag
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_documents d
    ON c.customer_id = d.customer_id
LEFT JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE c.customer_status = 'ACTIVE'
  AND (
        d.identity_document_status <> 'VALID'
        OR d.source_of_funds_status <> 'VALID'
        OR d.edd_file_status <> 'VALID'
        OR (
            c.customer_type = 'LEGAL_ENTITY'
            AND d.beneficial_ownership_status <> 'VALID'
        )
      )
  AND (
        m.onboarding_restriction_flag IS NULL
        OR m.onboarding_restriction_flag = 'NO'
      );


-- ============================================================
-- Test 4: Critical AML rating without escalation requirement
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    m.escalation_required_flag
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
LEFT JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE r.assigned_aml_rating = 'CRITICAL'
  AND (
        m.escalation_required_flag IS NULL
        OR m.escalation_required_flag = 'NO'
      );


-- ============================================================
-- Test 5: Restrictive measures applied but not reviewed
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    m.measure_type,
    m.restrictive_measure_status,
    m.last_measure_review_date
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN restrictive_measures m
    ON c.customer_id = m.customer_id
WHERE m.restrictive_measure_status = 'APPLIED'
  AND m.last_measure_review_date < CURRENT_DATE - INTERVAL '12 months';