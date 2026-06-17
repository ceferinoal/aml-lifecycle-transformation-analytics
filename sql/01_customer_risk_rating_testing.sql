/*
Project: AML Lifecycle Transformation Analytics
Module 01: Customer Risk Rating Testing

Objective:
Identify potential inconsistencies between customer AML risk factors and the assigned corporate AML rating.

Context:
The AML lifecycle starts at onboarding. If the customer risk rating does not reflect the real
risk factors of the customer, all downstream controls may be weakened: documentation,
EDD, restrictive measures, monitoring, reporting and escalation.
*/

-- ============================================================
-- Test 1: High-risk factors but LOW or MEDIUM AML rating
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    f.pep_flag,
    f.high_risk_country_flag,
    f.complex_ownership_flag,
    f.adverse_media_flag
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
      );


-- ============================================================
-- Test 2: PEP customers not classified as HIGH risk
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    f.pep_flag
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
WHERE f.pep_flag = 'YES'
  AND r.assigned_aml_rating <> 'HIGH';


-- ============================================================
-- Test 3: Customers in high-risk countries not classified as HIGH risk
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    f.high_risk_country_flag
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
WHERE f.high_risk_country_flag = 'YES'
  AND r.assigned_aml_rating <> 'HIGH';


-- ============================================================
-- Test 4: Legal entities with complex ownership not classified as HIGH risk
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    f.complex_ownership_flag
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
WHERE c.customer_type = 'LEGAL_ENTITY'
  AND f.complex_ownership_flag = 'YES'
  AND r.assigned_aml_rating <> 'HIGH';


-- ============================================================
-- Test 5: Repeated AML issues without rating escalation
-- ============================================================

SELECT
    c.customer_id,
    c.customer_type,
    c.country,
    r.assigned_aml_rating,
    r.last_rating_review_date,
    f.repeated_aml_issues_count
FROM customers c
JOIN aml_ratings r
    ON c.customer_id = r.customer_id
JOIN customer_risk_factors f
    ON c.customer_id = f.customer_id
WHERE f.repeated_aml_issues_count >= 3
  AND r.assigned_aml_rating IN ('LOW', 'MEDIUM');